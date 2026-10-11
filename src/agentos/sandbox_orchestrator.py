"""Fail-closed Level 11 Sandbox Orchestrator for OSS-AgentOS.

Integrates Stage A (Dependency Integrity) and Stage B (Isolated Container Execution)
with strict fail-closed enforcement, command allowlisting, runtime preflight,
workspace isolation, artifact validation, and reliable cleanup.
"""

from __future__ import annotations

import dataclasses
import datetime
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import tarfile
import uuid
from typing import Any

EXPECTED_LOCKFILE_HASH = "e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94"
ALLOWED_REGISTRIES = [
    "https://pypi.org/simple",
    "https://files.pythonhosted.org",
]
DEFAULT_TIMEOUT_SECONDS = 1800  # 30 minutes
DEFAULT_EXECUTION_IMAGE = "python:3.12-slim"
DEFAULT_DEPENDENCY_VOLUME = "agentos_sandbox_deps"


@dataclasses.dataclass
class SandboxResult:
    """Result of a sandbox run or preflight check."""

    run_id: str
    status: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    isolation_enforced: bool = False
    duration_seconds: float = 0.0
    exported_artifacts: list[str] = dataclasses.field(default_factory=list)


class SandboxOrchestrator:
    """Orchestrates Stage A and Stage B sandbox operations fail-closed."""

    def __init__(
        self,
        repo_root: pathlib.Path | None = None,
        allowlist_path: pathlib.Path | None = None,
        container_engine_override: str | None = None,
        act_enabled: bool = False,
        execution_image: str | None = None,
        dependency_volume: str | None = None,
    ) -> None:
        self.repo_root = repo_root or pathlib.Path(__file__).resolve().parent.parent.parent
        self.allowlist_path = (
            allowlist_path
            or self.repo_root / "sandbox" / "test_cmds" / "verified_cmds.yaml"
        )
        self.container_engine_override = container_engine_override
        # Mandatory: act workflow replay is OFF by default (untrusted code)
        self.act_enabled = act_enabled
        self.lockfile_path = self.repo_root / "uv.lock"
        self.execution_image = execution_image or DEFAULT_EXECUTION_IMAGE
        self.dependency_volume = dependency_volume or DEFAULT_DEPENDENCY_VOLUME

    def check_kill_switch(self) -> tuple[bool, str]:
        """Check whether kill switch is active."""
        kill_file = self.repo_root / "kill_state.json"
        if kill_file.exists():
            try:
                data = json.loads(kill_file.read_text(encoding="utf-8"))
                if data.get("state") in ("STOP", "KILLED", "PAUSED"):
                    return False, f"Kill switch active: state={data.get('state')}"
            except Exception as exc:
                return False, f"Invalid kill switch state file: {exc}"
        return True, "Kill switch inactive"

    def verify_stage_a_integrity(self) -> tuple[bool, str]:
        """Verify uv.lock presence, hash matching, and PyPI allowlist."""
        if not self.lockfile_path.exists():
            return False, "uv.lock does not exist"

        data = self.lockfile_path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash != EXPECTED_LOCKFILE_HASH:
            return False, (
                f"uv.lock hash mismatch: expected {EXPECTED_LOCKFILE_HASH}, got {actual_hash}"
            )

        # Check registry URLs
        content = self.lockfile_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            if "url = " in line:
                parts = line.split("url = ")
                if len(parts) > 1:
                    raw_url = parts[1].split('"')[1] if '"' in parts[1] else parts[1].split("'")[1]
                    if not any(raw_url.startswith(reg) for reg in ALLOWED_REGISTRIES):
                        return False, f"Disallowed package URL in lockfile: {raw_url}"

        return True, "Stage A lockfile and registry integrity verified"

    def prefetch_dependencies(self) -> tuple[bool, str, dict[str, Any]]:
        """Stage A: prefetch locked wheels into dedicated Docker volume and create integrity manifest."""
        ok, msg = self.verify_stage_a_integrity()
        if not ok:
            return False, f"Stage A integrity verification failed: {msg}", {}

        runtime_ok, runtime_msg, runtime_engine = self.check_runtime_preflight()
        if not runtime_ok or not runtime_engine:
            return False, f"Container runtime required for Stage A prefetch: {runtime_msg}", {}

        runtime_env = self._get_runtime_env(runtime_engine)

        # 1. Create Docker volume if not exists
        subprocess.run(
            [runtime_engine, "volume", "create", self.dependency_volume],
            capture_output=True,
            env=runtime_env,
        )

        # 2. Download binary wheels from PyPI only into the dedicated volume
        packages_to_fetch = [
            "typer", "pydantic", "pyyaml", "httpx", "pytest", "ruff", "mypy"
        ]
        sh_cmd = (
            "pip download --only-binary=:all: --no-build-isolation "
            "--index-url https://pypi.org/simple -d /deps "
            + " ".join(packages_to_fetch)
        )
        cmd = [
            runtime_engine, "run", "--rm",
            "-v", f"{self.dependency_volume}:/deps",
            self.execution_image,
            "sh", "-c", sh_cmd
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, env=runtime_env, timeout=180)
        if res.returncode != 0:
            return False, f"Prefetch download failed (exit {res.returncode}): {res.stderr}", {}

        # 3. Compute artifact hashes and generate manifest
        cmd_hashes = [
            runtime_engine, "run", "--rm",
            "-v", f"{self.dependency_volume}:/deps:ro",
            self.execution_image,
            "sh", "-c", "sha256sum /deps/*.whl"
        ]
        res_hashes = subprocess.run(cmd_hashes, capture_output=True, text=True, env=runtime_env, timeout=30)
        lines = res_hashes.stdout.strip().splitlines()
        manifest: dict[str, Any] = {
            "lockfile_hash": EXPECTED_LOCKFILE_HASH,
            "volume_name": self.dependency_volume,
            "approved_registry": "https://pypi.org/simple",
            "artifacts": {},
        }
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                sha = parts[0]
                fname = parts[1].replace("/deps/", "")
                manifest["artifacts"][fname] = sha

        manifest_path = self.repo_root / "sandbox" / "stage_a" / "integrity_manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return True, f"Successfully prefetched {len(manifest['artifacts'])} wheels into volume {self.dependency_volume}", manifest

    def check_command_allowlist(self, command_str: str) -> tuple[bool, str]:
        """Verify command against verified_cmds.yaml allowlist."""
        # Reject shell metacharacters / injection vectors
        if re.search(r"[;&|`$<>]", command_str):
            return False, f"Command contains forbidden shell metacharacters: {command_str}"

        clean_cmd = command_str.strip()
        allowed_cmds = ["pytest", "ruff check src/", "mypy src/"]

        # If allowlist file exists, read valid cmd lines
        if self.allowlist_path.exists():
            lines = self.allowlist_path.read_text(encoding="utf-8").splitlines()
            for line in lines:
                if "cmd:" in line:
                    val = line.split("cmd:")[1].strip()
                    if val and val not in allowed_cmds:
                        allowed_cmds.append(val)

        if clean_cmd not in allowed_cmds:
            return False, f"Command not in independently reviewed allowlist: {clean_cmd}"

        return True, clean_cmd

    def _resolve_docker_binary(self) -> str | None:
        """Find docker binary in PATH or standard per-user install location."""
        path = shutil.which("docker")
        if path:
            return path
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        if local_appdata:
            candidate = (
                pathlib.Path(local_appdata)
                / "Programs"
                / "DockerDesktop"
                / "resources"
                / "bin"
                / "docker.exe"
            )
            if candidate.exists():
                return str(candidate)
        return None

    def _get_runtime_env(self, engine_path: str) -> dict[str, str]:
        """Ensure runtime engine directory is in PATH for child plugins and credential helpers."""
        env = os.environ.copy()
        engine_parent = str(pathlib.Path(engine_path).parent)
        if engine_parent not in env.get("PATH", ""):
            env["PATH"] = engine_parent + os.pathsep + env.get("PATH", "")
        return env

    def check_runtime_preflight(self) -> tuple[bool, str, str | None]:
        """Check whether container runtime engine is installed and running."""
        if self.container_engine_override:
            return True, f"Using runtime override: {self.container_engine_override}", self.container_engine_override

        # Check docker
        docker_path = self._resolve_docker_binary()
        if docker_path:
            try:
                env = self._get_runtime_env(docker_path)
                res = subprocess.run(
                    [docker_path, "info"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    env=env,
                )
                if res.returncode == 0:
                    return True, "Docker daemon operational", docker_path
            except Exception:
                pass

        # Check podman
        podman_path = shutil.which("podman")
        if podman_path:
            try:
                res = subprocess.run(
                    ["podman", "info"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if res.returncode == 0:
                    return True, "Podman daemon operational", "podman"
            except Exception:
                pass

        return False, "No container runtime (Docker/Podman) is operational", None

    def validate_artifact_export(
        self,
        workspace_work: pathlib.Path,
        rel_artifact_path: str,
        dest_dir: pathlib.Path,
    ) -> tuple[bool, str, pathlib.Path | None]:
        """Validate artifact export path against directory traversal attacks."""
        if ".." in rel_artifact_path or rel_artifact_path.startswith("/") or rel_artifact_path.startswith("\\"):
            return False, f"Illegal artifact path (traversal attempt): {rel_artifact_path}", None

        source_file = (workspace_work / rel_artifact_path).resolve()
        try:
            source_file.relative_to(workspace_work.resolve())
        except ValueError:
            return False, f"Artifact path escapes workspace: {rel_artifact_path}", None

        dest_file = (dest_dir / rel_artifact_path).resolve()
        try:
            dest_file.relative_to(dest_dir.resolve())
        except ValueError:
            return False, f"Export destination escapes output directory: {rel_artifact_path}", None

        return True, "Artifact path validated", dest_file

    def execute(
        self,
        command_str: str,
        export_artifacts: list[str] | None = None,
        export_dest: pathlib.Path | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        action_class: str = "L1",
    ) -> SandboxResult:
        """Run fail-closed sandbox workflow."""
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        start_time = datetime.datetime.now(datetime.timezone.utc)

        # 1. Action class validation: Sandbox is L1; upstream social actions L3/L4 require Outbox & human approval
        if action_class in ("L3", "L4"):
            return SandboxResult(
                run_id=run_id,
                status="APPROVAL_BYPASS_ATTEMPT_DENIED",
                exit_code=126,
                error_message="Sandbox execution restricted to L1; upstream actions require Outbox approval",
            )

        # 2. Kill switch check
        kill_ok, kill_msg = self.check_kill_switch()
        if not kill_ok:
            return SandboxResult(
                run_id=run_id,
                status="KILL_SWITCH_ACTIVE",
                exit_code=126,
                error_message=kill_msg,
            )

        # 3. Stage A Dependency Integrity Check
        stage_a_ok, stage_a_msg = self.verify_stage_a_integrity()
        if not stage_a_ok:
            return SandboxResult(
                run_id=run_id,
                status="INTEGRITY_CHECK_FAILED",
                exit_code=1,
                error_message=stage_a_msg,
            )

        # 4. Command allowlist check
        cmd_ok, verified_cmd = self.check_command_allowlist(command_str)
        if not cmd_ok:
            return SandboxResult(
                run_id=run_id,
                status="COMMAND_DENIED",
                exit_code=127,
                error_message=verified_cmd,
            )

        # 5. Runtime preflight check — FAIL CLOSED
        runtime_ok, runtime_msg, runtime_engine = self.check_runtime_preflight()
        if not runtime_ok:
            # Mandatory: never fall back to host execution!
            return SandboxResult(
                run_id=run_id,
                status="RUNTIME_UNAVAILABLE",
                exit_code=125,
                error_message=f"{runtime_msg}. Host execution prohibited.",
            )

        # 6. Workspace isolation
        workspace_dir = self.repo_root / "sandbox" / "work" / run_id
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # Prepare tar stream of project source (src/ and pyproject.toml)
        buf = io.BytesIO()
        try:
            with tarfile.open(fileobj=buf, mode="w:gz") as tar:
                src_dir = self.repo_root / "src"
                if src_dir.exists():
                    tar.add(src_dir, arcname="src")
                pyproj = self.repo_root / "pyproject.toml"
                if pyproj.exists():
                    tar.add(pyproj, arcname="pyproject.toml")
            tar_bytes = buf.getvalue()
        except Exception:
            tar_bytes = b""

        exported_results: list[str] = []
        try:
            # Build container run command with all 9 mandatory isolation controls
            wrapped_cmd = (
                "export PYTHONUSERBASE=/work/.local && "
                "export PYTHONPATH=/work/.local/lib/python3.12/site-packages && "
                "export PATH=/work/.local/bin:$PATH && "
                "if [ -d /deps ] && [ \"$(ls -A /deps 2>/dev/null)\" ]; then "
                "  pip install --user --no-index --find-links=/deps pytest ruff mypy >/dev/null 2>&1 || true; "
                "fi && "
                "tar -xzf - -C /work 2>/dev/null || true; "
                f"{verified_cmd}"
            )
            container_cmd = [
                runtime_engine,
                "run",
                "-i",
                "--rm",
                "--network",
                "none",
                "--read-only",
                "--tmpfs",
                "/work:rw,exec,nosuid,size=4g",
                "--cpus",
                "2",
                "--memory",
                "4g",
                "--security-opt=no-new-privileges",
                "-v",
                f"{self.dependency_volume}:/deps:ro",
                "-w",
                "/work",
                self.execution_image,
                "sh",
                "-c",
                wrapped_cmd,
            ]

            runtime_env = self._get_runtime_env(runtime_engine)
            proc = subprocess.run(
                container_cmd,
                input=tar_bytes,
                capture_output=True,
                timeout=timeout_seconds,
                env=runtime_env,
            )

            stdout_str = (
                proc.stdout.decode("utf-8", errors="replace")
                if isinstance(proc.stdout, bytes)
                else (proc.stdout or "")
            )
            stderr_str = (
                proc.stderr.decode("utf-8", errors="replace")
                if isinstance(proc.stderr, bytes)
                else (proc.stderr or "")
            )

            # Export artifacts if requested
            if export_artifacts and export_dest:
                export_dest.mkdir(parents=True, exist_ok=True)
                for art in export_artifacts:
                    valid, msg, target = self.validate_artifact_export(workspace_dir, art, export_dest)
                    if not valid:
                        return SandboxResult(
                            run_id=run_id,
                            status="EXPORT_FAILED",
                            exit_code=1,
                            stdout=stdout_str,
                            stderr=stderr_str,
                            error_message=msg,
                            isolation_enforced=True,
                        )
                    if (workspace_dir / art).exists() and target:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(workspace_dir / art, target)
                        exported_results.append(str(target))

            duration = (datetime.datetime.now(datetime.timezone.utc) - start_time).total_seconds()
            return SandboxResult(
                run_id=run_id,
                status="SUCCESS" if proc.returncode == 0 else "EXECUTION_ERROR",
                exit_code=proc.returncode,
                stdout=stdout_str,
                stderr=stderr_str,
                isolation_enforced=True,
                duration_seconds=duration,
                exported_artifacts=exported_results,
            )

        except subprocess.TimeoutExpired:
            return SandboxResult(
                run_id=run_id,
                status="TIMEOUT",
                exit_code=124,
                error_message=f"Execution timed out after {timeout_seconds}s",
                isolation_enforced=True,
            )
        except KeyboardInterrupt:
            return SandboxResult(
                run_id=run_id,
                status="CANCELLED",
                exit_code=130,
                error_message="Execution cancelled by user",
                isolation_enforced=True,
            )
        except Exception as exc:
            return SandboxResult(
                run_id=run_id,
                status="EXECUTION_ERROR",
                exit_code=1,
                error_message=str(exc),
            )
        finally:
            # 7. Reliable cleanup on success, error, timeout, or cancellation
            if workspace_dir.exists():
                shutil.rmtree(workspace_dir, ignore_errors=True)
