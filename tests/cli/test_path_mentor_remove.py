"""CLI tests for path mentor removal."""
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


def test_mentor_remove(db_path):
    """Remove a mentor from a mentor project path (CLI + DB-backed)."""
    runner = CliRunner()
    # Add a path and associate a mentor (via CLI add then direct DB insert for mentor).
    add_result = runner.invoke(app_path, ["add", "--org", "test-org", "--project", "test-proj"])
    assert add_result.exit_code == 0, add_result.output
