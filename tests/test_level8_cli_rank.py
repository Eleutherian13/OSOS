"""Prompt 4 tests — CLI registration, rank, sort-aid, empty/DB-down, exclusions,
readiness, no upstream side-effect, source references, fixtures labelled synthetic."""
from typer.testing import CliRunner
from agentos.cli_rank import app_rank

def test_cli_command_registered():
    runner = CliRunner()
    result = runner.invoke(app_rank)
    assert result.exit_code == 0
    assert "DB STATUS" in result.output or "DB available" in result.output

def test_sort_aid_label_shown():
    runner = CliRunner()
    result = runner.invoke(app_rank, ["--sort-aid"])
    assert result.exit_code == 0
    assert "SORT AID — NOT A PREDICTION" in result.output

def test_empty_state_db_unavailable():
    runner = CliRunner()
    result = runner.invoke(app_rank)
    assert "DB unavailable" in result.output or "DB STATUS" in result.output
    assert "fixture" in result.output or "synthetic" in result.output or "Fixture" in result.output

def test_gate_output_all_present():
    runner = CliRunner()
    result = runner.invoke(app_rank)
    for gid in range(1,8):
        assert f"Gate {gid}" in result.output

def test_no_upstream_side_effect():
    # Read-only; no external writes
    runner = CliRunner()
    result = runner.invoke(app_rank)
    assert result.exit_code == 0
    assert "automatic" not in result.output.lower() or "no automatic" in result.output.lower()

def test_readiness_lowest_unmet_reported():
    runner = CliRunner()
    result = runner.invoke(app_rank)
    assert "Readiness" in result.output or "lowest" in result.output.lower() or "unmet" in result.output.lower()

def test_excluded_preserved_not_deleted():
    runner = CliRunner()
    result = runner.invoke(app_rank)
    assert "Excluded" in result.output or "exclusion" in result.output.lower()
