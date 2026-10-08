"""Migration runner for the AgentOS event store schema.

Migrations are plain SQL files in the ``migrations/`` directory named
``V<sequence>__<description>.sql``. They are executed in order, exactly once,
against the configured database. The runner supports three operations:

- :func:`run` — apply pending migrations (development/CI use).
- :func:`run_and_dump` — apply pending migrations and export the current
  schema for idempotency verification.
- :func:`dump` — export the current schema without running any migration.

No ORM is used: the SQL is executed verbatim so it is debuggable directly with
``psql``.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

import psycopg

from .config import DatabaseConfig
from .connection import Connection, _message_from_error
from .errors import MigrationError


MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "migrations"
MIGRATION_RE = re.compile(r"^V(\d+)__(.+)\.sql$")


class _Migration:
    __slots__ = ("sequence", "name", "path")

    def __init__(self, path: Path) -> None:
        match = MIGRATION_RE.match(path.name)
        if match is None:
            raise MigrationError(f"migration file has unsupported name: {path.name!r}")
        self.sequence = int(match.group(1))
        self.name = match.group(2)
        self.path = path


def _list_migrations(migrations_dir: Path = MIGRATIONS_DIR) -> list[_Migration]:
    """Return all migration files, sorted by their sequence number."""
    if not migrations_dir.exists():
        raise MigrationError(f"migrations directory not found: {migrations_dir!r}")
    migrations: list[_Migration] = []
    for path in migrations_dir.iterdir():
        if path.is_file() and fnmatch.fnmatch(path.name, "V*_*.sql"):
            migrations.append(_Migration(path))
    migrations.sort(key=lambda m: m.sequence)
    return migrations


def _ensure_registry(connection: psycopg.Connection[dict[str, Any]]) -> None:
    """Create the migration registry table if it does not exist."""
    connection.execute("""
        create table if not exists db_migrations (
            id            serial primary key,
            version       integer not null,
            applied_at    timestamp with time zone not null default now()
        )
    """)


def _installed(connection: psycopg.Connection[dict[str, Any]]) -> set[int]:
    """Return the set of migration sequences already applied."""
    _ensure_registry(connection)
    with connection.cursor() as cursor:
        cursor.execute("select version from db_migrations order by version")
        return {row["version"] for row in cursor.fetchall()}


def run(config: DatabaseConfig, migrations_dir: Path | None = None) -> list[str]:
    """Apply all pending migrations.

    Returns the names of migrations that were applied.
    """
    migrations_dir = migrations_dir or MIGRATIONS_DIR
    applied: list[str] = []
    with Connection(config) as connection:
        connection.execute("set statement_timeout = '30s'")
        with connection:
            installed = _installed(connection._conn)  # type: ignore[union-attr]
            for migration in _list_migrations(migrations_dir):
                if migration.sequence in installed:
                    continue
                sql = migration.path.read_text(encoding="utf-8")
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                cursor.execute(
                    "insert into db_migrations (version) values (%s)",
                    (migration.sequence,),
                )
            applied = [m.name for m in _list_migrations(migrations_dir)]
    return applied


def dump(config: DatabaseConfig, migrations_dir: Path | None = None) -> str:
    """Export the current schema of the migrations database.

    The schema dump is the deterministic artifact used to verify that
    migrations are idempotent: running them again must leave this dump
    byte-identical.
    """
    migrations_dir = migrations_dir or MIGRATIONS_DIR
    migrations = _list_migrations(migrations_dir)
    applied = sorted({m.sequence for m in migrations})
    with Connection(config) as connection:
        _ensure_registry(connection._conn)  # type: ignore[arg-type]
        with connection:
            for migration in migrations:
                connection.execute(
                    "insert into db_migrations (version) values (%s)",
                    (migration.sequence,),
                )
            with connection.cursor() as cursor:
                cursor.execute(
                    "select table_name from information_schema.tables "
                    "where table_schema = 'public' "
                    "order by table_name"
                )
                tables = [row["table_name"] for row in cursor.fetchall()]
        if not tables:
            return ""
        parts: list[str] = []
        for table_name in tables:
            if table_name == "db_migrations":
                continue
            columns: list[str] = []
            with connection.cursor(name=f"col_{table_name}") as col_cursor:
                col_cursor.execute(
                    """
                    select
                        attname,
                        format_type(atttypid, atttypmod),
                        coalesce(pg_get_expr(adbin, adrelid), '') as default_expr,
                        not attnotnull as nullable
                    from pg_attribute
                    where attrelid = %s::regclass
                      and attnum > 0
                      and not attisdropped
                    order by attnum
                    """,
                    (table_name,),
                )
                for col in col_cursor:
                    name = col["attname"]
                    typ = col["format_type"]
                    default = col["default_expr"].replace("'", "''")
                    nullable = "null" if col["nullable"] else "not null"
                    default_clause = f" default '{default}'" if default else ""
                    columns.append(f"    {name} {typ} {nullable}{default_clause}")
            parts.append(f"create table {table_name} (\n" + ",\n".join(columns) + "\n);")
        return "\n".join(parts) + "\n"
