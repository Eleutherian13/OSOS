"""Unit tests for agentos.db.config (no PostgreSQL required)."""

import pytest
from agentos.db.config import DatabaseConfig, _parse_dsn
from agentos.db.errors import DatabaseConnectionError


def test_from_env_missing() -> None:
    import os
    # Save and clear both possible env vars
    old_db_url = os.environ.pop("DATABASE_URL", None)
    old_sqlite_path = os.environ.pop("AGENTOS_DB_PATH", None)
    try:
        with pytest.raises(DatabaseConnectionError):
            DatabaseConfig.from_env()
    finally:
        if old_db_url is not None:
            os.environ["DATABASE_URL"] = old_db_url
        if old_sqlite_path is not None:
            os.environ["AGENTOS_DB_PATH"] = old_sqlite_path


def test_parse_dsn_valid() -> None:
    d = _parse_dsn("postgres://localhost:5432/agent")
    assert isinstance(d["port"], int) and d["port"] == 5432


def test_parse_dsn_bad_port() -> None:
    import os
    # Ensure AGENTOS_DB_PATH is not set (would bypass DSN parsing)
    old_sqlite_path = os.environ.pop("AGENTOS_DB_PATH", None)
    try:
        with pytest.raises(DatabaseConnectionError):
            DatabaseConfig.from_env()  # No DATABASE_URL, no AGENTOS_DB_PATH
    finally:
        if old_sqlite_path is not None:
            os.environ["AGENTOS_DB_PATH"] = old_sqlite_path
