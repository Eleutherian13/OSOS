"""Test suite for Level 11 Sandbox Orchestrator and CLI Integration.

Tests required by OSS-AgentOS Level 11:
- successful execution
- failed prefetch
- missing runtime (fail-closed, no host fallback)
- stale or tampered lockfile
- denied command (not in allowlist)
- denied command (shell injection)
- timeout enforcement
- cancellation enforcement
- failed export (path traversal attempt)
- approval bypass attempt (L3/L4 upstream without approval)
- kill switch enforcement
- CLI commands: preflight and run
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from agentos.cli import app
from agentos.sandbox_orchestrator import (
    EXPECTED_LOCKFILE_HASH,
    SandboxOrchestrator,
    SandboxResult,
)

runner = CliRunner()


def test_missing_runtime_fails_closed(tmp_path: pathlib.Path) -> None:
    """Missing runtime must fail closed immediately with code 125, never running on host."""
    orchestrator = SandboxOrchestrator()
    with patch.object(orchestrator, "check_runtime_preflight", return_value=(False, "No daemon", None)):
        res = orchestrator.execute("pytest")
        assert res.status == "RUNTIME_UNAVAILABLE"
        assert res.exit_code == 125
        assert "Host execution prohibited" in res.error_message


def test_stale_or_tampered_lockfile(tmp_path: pathlib.Path) -> None:
    """A modified/stale lockfile must fail Stage A integrity check immediately."""
    fake_lock = tmp_path / "uv.lock"
    fake_lock.write_text("tampered content", encoding="utf-8")

    orchestrator = SandboxOrchestrator()
    orchestrator.lockfile_path = fake_lock
    res = orchestrator.execute("pytest")
    assert res.status == "INTEGRITY_CHECK_FAILED"
    assert res.exit_code == 1
    assert "mismatch" in res.error_message


def test_denied_command_not_in_allowlist() -> None:
    """Commands outside verified_cmds.yaml must be rejected fail-closed with code 127."""
    orchestrator = SandboxOrchestrator()
    res = orchestrator.execute("curl https://evil.com")
    assert res.status == "COMMAND_DENIED"
    assert res.exit_code == 127
    assert "independently reviewed allowlist" in res.error_message


def test_denied_command_shell_injection() -> None:
    """Commands containing shell metacharacters must be rejected immediately."""
    orchestrator = SandboxOrchestrator()
    res = orchestrator.execute("pytest; rm -rf /")
    assert res.status == "COMMAND_DENIED"
    assert res.exit_code == 127
    assert "shell metacharacters" in res.error_message


def test_approval_bypass_attempt() -> None:
    """Attempting L3/L4 upstream actions via sandbox must be rejected (only L1 allowed)."""
    orchestrator = SandboxOrchestrator()
    res = orchestrator.execute("pytest", action_class="L3")
    assert res.status == "APPROVAL_BYPASS_ATTEMPT_DENIED"
    assert res.exit_code == 126
    assert "Outbox approval" in res.error_message


def test_kill_switch_active(tmp_path: pathlib.Path) -> None:
    """Active kill switch must stop execution before any action."""
    orchestrator = SandboxOrchestrator()
    with patch.object(orchestrator, "check_kill_switch", return_value=(False, "Kill switch active: state=STOP")):
        res = orchestrator.execute("pytest")
        assert res.status == "KILL_SWITCH_ACTIVE"
        assert res.exit_code == 126


def test_successful_execution() -> None:
    """When runtime is operational, command runs in container and captures results."""
    orchestrator = SandboxOrchestrator(container_engine_override="docker")
    fake_proc = MagicMock(returncode=0, stdout="test passed", stderr="")

    with (
        patch.object(orchestrator, "verify_stage_a_integrity", return_value=(True, "ok")),
        patch("subprocess.run", return_value=fake_proc) as mock_run,
    ):
        res = orchestrator.execute("pytest")
        assert res.status == "SUCCESS"
        assert res.exit_code == 0
        assert res.stdout == "test passed"
        assert res.isolation_enforced is True
        # Verify mandatory container isolation flags were passed
        mock_cmd = mock_run.call_args[0][0]
        assert "--network" in mock_cmd
        assert "none" in mock_cmd
        assert "--read-only" in mock_cmd
        assert "--tmpfs" in mock_cmd
        assert "--cpus" in mock_cmd
        assert "--memory" in mock_cmd


def test_timeout_enforcement() -> None:
    """Subprocess timeout must be handled cleanly with status TIMEOUT and code 124."""
    orchestrator = SandboxOrchestrator(container_engine_override="docker")
    with (
        patch.object(orchestrator, "verify_stage_a_integrity", return_value=(True, "ok")),
        patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="pytest", timeout=5)),
    ):
        res = orchestrator.execute("pytest", timeout_seconds=5)
        assert res.status == "TIMEOUT"
        assert res.exit_code == 124
        assert "timed out" in res.error_message


def test_cancellation_enforcement() -> None:
    """User cancellation (KeyboardInterrupt) must produce CANCELLED and code 130."""
    orchestrator = SandboxOrchestrator(container_engine_override="docker")
    with (
        patch.object(orchestrator, "verify_stage_a_integrity", return_value=(True, "ok")),
        patch("subprocess.run", side_effect=KeyboardInterrupt()),
    ):
        res = orchestrator.execute("pytest")
        assert res.status == "CANCELLED"
        assert res.exit_code == 130


def test_failed_artifact_export_traversal(tmp_path: pathlib.Path) -> None:
    """Path traversal during artifact export must be blocked."""
    orchestrator = SandboxOrchestrator(container_engine_override="docker")
    fake_proc = MagicMock(returncode=0, stdout="ok", stderr="")
    with (
        patch.object(orchestrator, "verify_stage_a_integrity", return_value=(True, "ok")),
        patch("subprocess.run", return_value=fake_proc),
    ):
        res = orchestrator.execute(
            "pytest",
            export_artifacts=["../../escape.txt"],
            export_dest=tmp_path / "out",
        )
        assert res.status == "EXPORT_FAILED"
        assert res.exit_code == 1
        assert "traversal attempt" in res.error_message


def test_cli_sandbox_preflight() -> None:
    """CLI preflight command exits 0 and reports READY when Docker daemon is operational."""
    result = runner.invoke(app, ["sandbox", "preflight"])
    assert "=== Sandbox Preflight Checks ===" in result.output
    # Docker Desktop is operational on this host; preflight must succeed
    assert result.exit_code == 0, (
        f"Expected preflight READY (exit 0) with Docker Desktop running; got:\n{result.output}"
    )
    assert "Preflight result: READY" in result.output


def test_cli_sandbox_preflight_blocked() -> None:
    """CLI preflight exits 1 and reports BLOCKED when no container runtime is available."""
    from unittest.mock import patch
    from agentos.sandbox_orchestrator import SandboxOrchestrator

    with patch.object(
        SandboxOrchestrator, "check_runtime_preflight",
        return_value=(False, "No daemon available", None),
    ):
        result = runner.invoke(app, ["sandbox", "preflight"])
    assert "=== Sandbox Preflight Checks ===" in result.output
    assert result.exit_code == 1
    assert "Preflight result: BLOCKED" in result.output


def test_cli_sandbox_run_denied_command() -> None:
    """CLI run command denies unallowlisted command."""
    result = runner.invoke(app, ["sandbox", "run", "curl https://bad.com"])
    assert result.exit_code == 127
    assert "Status: COMMAND_DENIED" in result.output


def test_stage_a_missing_lockfile(tmp_path: pathlib.Path) -> None:
    """Missing lockfile must fail Stage A integrity check immediately."""
    orchestrator = SandboxOrchestrator()
    orchestrator.lockfile_path = tmp_path / "nonexistent.lock"
    ok, msg = orchestrator.verify_stage_a_integrity()
    assert not ok
    assert "does not exist" in msg


def test_stage_a_disallowed_source(tmp_path: pathlib.Path) -> None:
    """Lockfile referencing a disallowed registry must fail Stage A integrity check."""
    fake_lock = tmp_path / "uv.lock"
    content = 'url = "https://unauthorized-mirror.evil.org/simple/pkg.whl"\n'
    fake_lock.write_text(content, encoding="utf-8")
    content_hash = hashlib.sha256(fake_lock.read_bytes()).hexdigest()

    orchestrator = SandboxOrchestrator()
    orchestrator.lockfile_path = fake_lock
    with patch("agentos.sandbox_orchestrator.EXPECTED_LOCKFILE_HASH", content_hash):
        ok, msg = orchestrator.verify_stage_a_integrity()
        assert not ok
        assert "Disallowed package URL" in msg


def test_cli_sandbox_run_allowed_command_live() -> None:
    """CLI run command executes allowlisted smoke command 'true' in live Stage B container."""
    result = runner.invoke(app, ["sandbox", "run", "true"])
    assert result.exit_code == 0
    assert "Status: SUCCESS" in result.output
