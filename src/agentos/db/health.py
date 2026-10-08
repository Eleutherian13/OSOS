"""Health check for the AgentOS event store.

A single ``is_healthy`` function that probes actual PostgreSQL connectivity
and schema readiness. Used by integration tests and development tooling. It
never prints secrets or credentials.
"""

from __future__ import annotations

from dataclasses import dataclass

import psycopg

from .config import DatabaseConfig, _parse_dsn
from .connection import Connection, _message_from_error
from .errors import DatabaseConnectionError, DatabaseError


@dataclass(frozen=True)
class HealthResult:
    """Result of a database health check.

    Attributes:
        healthy: True when the database is reachable and migrations are
            applied.
        error: A human-readable error description when not healthy.
    """

    healthy: bool
    error: str | None = None


def is_healthy(config: DatabaseConfig, migrations_applied: bool = True) -> HealthResult:
    """Check that the database is reachable and optionally that schema exists.

    A ``connection`` error means the host/port/database cannot be reached.
    A ``schema`` error means the database is reachable but the ``event_store``
    table is not present, which usually means migrations have not run.
    """
    try:
        with Connection(config) as connection:
            connection.execute("select 1 as healthy")
            result = connection.fetchone()
            if result is None or result.get("healthy") != 1:
                return HealthResult(healthy=False, error="database returned unexpected result")
            if migrations_applied:
                connection.execute(
                    "select exists(select 1 from information_schema.tables "
                    "where table_schema = 'public' and table_name = 'event_store') as has_table"
                )
                row = connection.fetchone()
                if not row or not row.get("has_table"):
                    return HealthResult(
                        healthy=False,
                        error="event store schema not present; run database migrations first",
                    )
    except DatabaseConnectionError as exc:
        return HealthResult(healthy=False, error=f"connection failed: {exc}")
    except psycopg.Error as exc:
        return HealthResult(healthy=False, error=_message_from_error(exc))
    return HealthResult(healthy=True, error=None)
