"""CLI smoke tests for the Level 0 bootstrap."""

import re

from typer.testing import CliRunner

from agentos.cli import app

runner = CliRunner()


def test_help_flag_starts_and_prints_usage() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_bare_invocation_prints_help() -> None:
    """Bare `agentos` shows full help; click treats it as a usage error (exit 2)."""
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "Usage:" in result.output


def test_version_command_prints_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.output.startswith("agentos ")


def test_version_flag_prints_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.startswith("agentos ")


def test_version_format_is_semver_like() -> None:
    """The version output follows X.Y.Z (or X.Y)."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    match = re.fullmatch(
        r"agentos \d+\.\d+(\.\d+)? \(Python [\d.]+\)", result.output.rstrip()
    )
    assert match, f"unexpected version output: {result.output!r}"


def test_unknown_command_fails_cleanly() -> None:
    """An unknown command must exit non-zero with a usage error, not a traceback."""
    result = runner.invoke(app, ["definitely-not-a-command"])
    assert result.exit_code == 2
    assert "No such command" in result.output
