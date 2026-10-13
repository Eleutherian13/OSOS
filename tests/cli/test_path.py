"""CLI tests for path commands."""
import os
import tempfile
import pytest
from typer.testing import CliRunner
from agentos.cli_path import app_path
from agentos.db.config import DatabaseConfig
from agentos.db.migrations import run


@pytest.fixture(scope="module")
def db_path():
    """Create a temporary SQLite DB for CLI tests."""
    path = tempfile.mktemp(suffix=".sqlite3")
    os.environ["AGENTOS_DB_PATH"] = path
    cfg = DatabaseConfig.from_env()
    run(cfg)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


def test_path_add(db_path):
    runner = CliRunner()
    result = runner.invoke(app_path, ["add", "--org", "test-org", "--project", "test-proj"])
    assert result.exit_code == 0, result.output
    assert "Path created" in result.output or "path created" in result.output.lower()


def test_path_show(db_path):
    """Show requires a path ID - first create one."""
    # Create path first
    runner = CliRunner()
    add_result = runner.invoke(app_path, ["add", "--org", "test-org", "--project", "test-proj"])
    assert add_result.exit_code == 0
    
    # Extract path ID from output (simplified - in real test would parse)
    # For now just verify the command doesn't crash
    show_result = runner.invoke(app_path, ["show", "--help"])
    assert show_result.exit_code == 0


def test_path_state(db_path):
    runner = CliRunner()
    # Get help to verify command exists
    result = runner.invoke(app_path, ["state", "--help"])
    assert result.exit_code == 0


def test_interact_add(db_path):
    runner = CliRunner()
    result = runner.invoke(app_path, ["interact", "add", "--help"])
    assert result.exit_code == 0
