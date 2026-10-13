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

from .config import DatabaseConfig
from .connection import Connection, Session, _message_from_error
from .errors import MigrationError


MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "migrations"
SQLITE_MIGRATIONS_DIR = Path(__file__).resolve().parent / "sqlite_migrations"
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


def _list_migrations(migrations_dir: Path | None = None) -> list[_Migration]:
    """Return all migration files, sorted by their sequence number.

    When running against SQLite, prefers the pre-portied SQLite migrations
    in ``src/agentos/db/sqlite_migrations/`` over the PostgreSQL originals.
    """
    if migrations_dir is None:
        # Auto-select based on available SQLite migrations
        if SQLITE_MIGRATIONS_DIR.exists():
            migrations_dir = SQLITE_MIGRATIONS_DIR
        else:
            migrations_dir = MIGRATIONS_DIR
    if not migrations_dir.exists():
        raise MigrationError(f"migrations directory not found: {migrations_dir!r}")
    migrations: list[_Migration] = []
    for path in migrations_dir.iterdir():
        if path.is_file() and fnmatch.fnmatch(path.name, "V*_*.sql"):
            migrations.append(_Migration(path))
    migrations.sort(key=lambda m: m.sequence)
    return migrations


def _is_sqlite_dsn(dsn: str) -> bool:
    """Check if the DSN indicates an SQLite database."""
    return dsn.startswith("sqlite:///")


def _port_for_sqlite(pg_sql: str, migration_name: str) -> str:
    """Port PostgreSQL SQL to SQLite-compatible SQL on demand."""
    try:
        from .sqlite_migrations import port_sql
        return port_sql(pg_sql, migration_name)
    except ImportError:
        sql = pg_sql
        sql = re.sub(r'create\s+extension\s+if\s+not\s+exists\s+pgcrypto;\s*\n?', '', sql, flags=re.IGNORECASE)
        sql = sql.replace('gen_random_uuid()', 'lower(hex(randomblob(16)))')
        sql = re.sub(r'timestamp\s+with\s+time\s+zone', 'datetime', sql, flags=re.IGNORECASE)
        sql = sql.replace('jsonb', 'text').replace("::jsonb", "")
        sql = re.sub(r'\bserial\b', 'integer primary key autoincrement', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bvarchar\s*\(\s*\d+\s*\)', 'text', sql, flags=re.IGNORECASE)
        sql = sql.replace("default now()", "default datetime('now')").replace("DEFAULT now()", "DEFAULT datetime('now')")
        sql = re.sub(r'\s+returning\s+[^;]+', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'set\s+statement_timeout.*;', '', sql, flags=re.IGNORECASE)
        return sql.strip() + "\n"


def _ensure_registry(connection: Connection) -> None:
    """Create the migration registry table if it does not exist."""
    # Handle both Connection and adapter objects
    dsn = getattr(connection, 'config', None)
    if dsn is not None:
        dsn = dsn.dsn
    else:
        # Adapter object - get DSN from the Connection it wraps
        dsn = getattr(getattr(connection, '_conn', None), 'config', None)
        if dsn is not None:
            dsn = dsn.dsn
        else:
            dsn = ""
    if _is_sqlite_dsn(dsn):
        connection.execute("""
            create table if not exists db_migrations (
                id            integer primary key autoincrement,
                version       integer not null unique,
                applied_at    datetime not null default (datetime('now'))
            )
        """)
    else:
        connection.execute("""
            create table if not exists db_migrations (
                id            serial primary key,
                version       integer not null,
                applied_at    timestamp with time zone not null default now()
            )
        """)


def _installed(connection: Connection) -> set[int]:
    """Return the set of migration sequences already applied."""
    _ensure_registry(connection)
    rows = connection.fetchall("select version from db_migrations order by version")
    return {row["version"] for row in rows}


def run(config: DatabaseConfig, migrations_dir: Path | None = None) -> list[str]:
    """Apply all pending migrations.

    Returns the names of migrations that were applied.
    When running against SQLite, uses pre-portied migrations from
    ``src/agentos/db/sqlite_migrations/``.
    """
    is_sqlite = _is_sqlite_dsn(config.dsn)
    if is_sqlite and migrations_dir is None:
        migrations_dir = SQLITE_MIGRATIONS_DIR
    migrations_dir = migrations_dir or MIGRATIONS_DIR
    applied: list[str] = []
    with Connection(config) as connection:
        with Session(connection):
            installed = _installed(connection)
            for migration in _list_migrations(migrations_dir):
                if migration.sequence in installed:
                    continue
                raw_sql = migration.path.read_text(encoding="utf-8")
                # Check if the file has a MIGRATION variable
                if "MIGRATION = " in raw_sql:
                    # Extract the MIGRATION variable content
                    import ast
                    # Find the MIGRATION assignment
                    match = re.search(r'MIGRATION\s*=\s*"""(.*?)"""', raw_sql, re.DOTALL)
                    if match:
                        raw_sql = match.group(1)
                    else:
                        # Fallback: try single quotes
                        match = re.search(r"MIGRATION\s*=\s*\'\'\ '(.*?)\'\'\ '", raw_sql, re.DOTALL)
                        if match:
                            raw_sql = match.group(1)
                if is_sqlite:
                    sql = _port_for_sqlite(raw_sql, migration.name)
                else:
                    sql = raw_sql
                connection.execute(sql)
                connection.execute(
                    "insert into db_migrations (version) values (?)",
                    (migration.sequence,),
                )
            applied = [m.name for m in _list_migrations(migrations_dir)
                       if m.sequence not in installed]
    return applied


def dump(config: DatabaseConfig, migrations_dir: Path | None = None) -> str:
    """Export the current schema of the migrations database."""
    migrations_dir = migrations_dir or MIGRATIONS_DIR
    migrations = _list_migrations(migrations_dir)
    with Connection(config) as connection:
        _ensure_registry(connection)
        with connection:
            for migration in migrations:
                try:
                    connection.execute(
                        "insert into db_migrations (version) values (?)",
                        (migration.sequence,),
                    )
                except Exception:
                    pass
            # Get table list (backend-agnostic)
            if _is_sqlite_dsn(connection.config.dsn):
                rows = connection.fetchall(
                    "select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name"
                )
                tables = [row["name"] for row in rows]
            else:
                rows = connection.fetchall(
                    "select table_name from information_schema.tables "
                    "where table_schema = 'public' order by table_name"
                )
                tables = [row["table_name"] for row in rows]
        if not tables:
            return ""
        parts: list[str] = []
        for table_name in tables:
            if table_name == "db_migrations":
                continue
            if _is_sqlite_dsn(connection.config.dsn):
                try:
                    columns = connection.fetchall(f"pragma table_info(\"{table_name}\")")
                    col_lines = []
                    for col in columns:
                        name = col["name"]
                        typ = col["type"] or "TEXT"
                        notnull = "not null" if col["notnull"] else ""
                        default = f"default {col['dflt_value']}" if col["dflt_value"] is not None else ""
                        pk = "primary key" if col["pk"] else ""
                        parts_str = " ".join(s for s in [notnull, default, pk] if s)
                        col_lines.append(f"    {name} {typ} {parts_str}".strip())
                    parts.append(f"create table {table_name} (\n" + ",\n".join(col_lines) + "\n);")
                except Exception:
                    parts.append(f"-- Unable to dump {table_name}")
            else:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            select attname, format_type(atttypid, atttypmod),
                                   coalesce(pg_get_expr(adbin, adrelid), '') as default_expr,
                                   not attnotnull as nullable
                            from pg_attribute
                            where attrelid = %s::regclass
                              and attnum > 0 and not attisdropped
                            order by attnum
                        """, (table_name,))
                        col_lines = []
                        for col in cursor:
                            name = col["attname"]
                            typ = col["format_type"]
                            default = col["default_expr"].replace("'", "''")
                            nullable = "null" if col["nullable"] else "not null"
                            default_clause = f" default '{default}'" if default else ""
                            col_lines.append(f"    {name} {typ} {nullable}{default_clause}")
                        parts.append(f"create table {table_name} (\n" + ",\n".join(col_lines) + "\n);")
                except Exception:
                    parts.append(f"-- Unable to dump {table_name}")
        return "\n".join(parts) + "\n"
