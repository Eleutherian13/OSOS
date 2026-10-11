"""End-to-End and Adversarial Regression Tests for Level 11 Stage A and Stage B."""

from __future__ import annotations

import json
import pathlib
import subprocess
from unittest.mock import MagicMock, patch

from agentos.sandbox_orchestrator import (
    EXPECTED_LOCKFILE_HASH,
    SandboxOrchestrator,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_stage_a_integrity_manifest_and_lockfile_hash() -> None:
    """Stage A integrity manifest must exist and match EXPECTED_LOCKFILE_HASH."""
    manifest_path = REPO_ROOT / "sandbox" / "stage_a" / "integrity_manifest.json"
    assert manifest_path.exists(), "integrity_manifest.json must be generated"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["lockfile_hash"] == EXPECTED_LOCKFILE_HASH
    assert manifest["volume_name"] == "agentos_sandbox_deps"
    assert manifest["approved_registry"] == "https://pypi.org/simple"
    assert len(manifest["artifacts"]) > 0

    # Cross check hashes against uv.lock
    uv_lock_content = (REPO_ROOT / "uv.lock").read_text(encoding="utf-8")
    matched = sum(1 for sha in manifest["artifacts"].values() if sha in uv_lock_content)
    assert matched >= 20, f"Expected majority of artifact hashes to match uv.lock, got {matched}"


def test_stage_b_uses_readonly_dependency_volume_and_no_network() -> None:
    """Stage B invocation must strictly enforce --network none and :ro dependency mount."""
    orchestrator = SandboxOrchestrator()
    captured_cmds: list[list[str]] = []

    def mock_subprocess_run(cmd, *args, **kwargs):
        captured_cmds.append(cmd)
        mock = MagicMock()
        mock.returncode = 0
        mock.stdout = b"mock ok"
        mock.stderr = b""
        return mock

    with (
        patch.object(orchestrator, "check_runtime_preflight", return_value=(True, "ok", "docker")),
        patch.object(orchestrator, "verify_stage_a_integrity", return_value=(True, "ok")),
        patch("subprocess.run", side_effect=mock_subprocess_run),
    ):
        res = orchestrator.execute("true")
        assert res.status == "SUCCESS"

    assert len(captured_cmds) == 1
    cmd = captured_cmds[0]
    assert "--network" in cmd and cmd[cmd.index("--network") + 1] == "none"
    assert "--read-only" in cmd
    assert "--tmpfs" in cmd and "/work:rw,exec,nosuid,size=4g" in cmd[cmd.index("--tmpfs") + 1]

    # Verify dependency volume is mounted strictly read-only (:ro)
    assert "-v" in cmd
    vol_mount = cmd[cmd.index("-v") + 1]
    assert vol_mount.endswith(":/deps:ro")

    # Verify no host directory bind mounts
    for arg in cmd:
        if arg.startswith("-v"):
            val = cmd[cmd.index(arg) + 1] if arg == "-v" else arg.split("-v")[1]
            assert not (":\\" in val or "/Users/" in val or "/home/" in val), f"Host bind mount forbidden: {val}"


def test_stage_a_prefetch_unauthorized_registry_fails_closed(tmp_path: pathlib.Path) -> None:
    """Prefetch must reject untrusted registry fail-closed."""
    orchestrator = SandboxOrchestrator()
    fake_lock = tmp_path / "uv.lock"
    fake_lock.write_text('url = "https://untrusted-pypi.evil.org/simple/pkg.whl"\n', encoding="utf-8")
    orchestrator.lockfile_path = fake_lock

    ok, msg, manifest = orchestrator.prefetch_dependencies()
    assert not ok
    assert "integrity verification failed" in msg


def test_missing_dependency_volume_fails_closed() -> None:
    """If dependency volume is not available or corrupt, execution must fail closed without host execution."""
    orchestrator = SandboxOrchestrator(dependency_volume="nonexistent_corrupt_volume_99999")
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["docker"])):
        res = orchestrator.execute("pytest")
        assert res.status == "RUNTIME_UNAVAILABLE"
        assert res.exit_code == 125
        assert res.isolation_enforced is False


def test_live_stage_b_offline_tool_execution() -> None:
    """Live Stage B execution of allowlisted smoke commands inside Docker Desktop with offline deps."""
    orchestrator = SandboxOrchestrator()
    res = orchestrator.execute("true")
    assert res.status == "SUCCESS"
    assert res.exit_code == 0
    assert res.isolation_enforced is True

    res_id = orchestrator.execute("id")
    assert res_id.status == "SUCCESS"
    assert res_id.exit_code == 0
    assert "uid=" in res_id.stdout
