"""Connection handling for the AgentOS event store.

All database access goes through this module. Raw ``psycopg`` calls are never
made directly by callers. Connections are acquired lazily and closed on
explicit use or on garbage collection.
"""

from __future__ import annotations

import contextlib
import os
import socket
import uuid
from collections.abc import AsyncIterator, Iterator
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from functools import partial

from .config import DatabaseConfig, _parse_dsn
from .errors import DatabaseConnectionError, UnknownDatabaseDriver


class _Psycopg2Adapter:
    """Adapts a psycopg2 connection to the psycopg3 API used by Connection.

    psycopg3 exposes execute/fetchone/fetchall directly on the connection.
    psycopg2 requires a cursor. This wrapper provides the same interface.
    """

    __slots__ = ("_conn", "_cursor")

    def __init__(self, conn: Any) -> None:
        self._conn = conn
        self._cursor: Any | None = None

    def close(self) -> None:
        self._conn.close()

    @property
    def autocommit(self) -> bool:
        return self._conn.autocommit

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        self._conn.autocommit = bool(value)

    def _ensure_cursor(self) -> Any:
        if self._cursor is None or self._cursor.closed:
            self._cursor = self._conn.cursor()
        return self._cursor

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> None:
        cur = self._ensure_cursor()
        cur.execute(sql, params or ())

    def fetchone(self, sql: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        cur = self._ensure_cursor()
        cur.execute(sql, params or ())
        row = cur.fetchone()
        return dict(row) if row is not None else None

    def fetchall(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        cur = self._ensure_cursor()
        cur.execute(sql, params or ())
        return [dict(r) for r in cur.fetchall()]

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def executemany(self, sql: str, params_list: list[tuple[Any, ...]]) -> None:
        """Execute a statement against multiple parameter sets."""
        cur = self._ensure_cursor()
        cur.executemany(sql, params_list)

    def cursor(self) -> Any:
        """Return a cursor for direct SQL execution."""
        return self._ensure_cursor()


class _SQLiteAdapter:
    """Adapts a sqlite3 connection to the psycopg3 API used by Connection.

    sqlite3 exposes execute/fetchone/fetchall on cursors, not directly on
    the connection. This wrapper provides the same interface as _Psycopg2Adapter.
    """

    __slots__ = ("_conn", "_cursor")

    def __init__(self, conn: Any) -> None:
        self._conn = conn
        self._cursor: Any | None = None

    def close(self) -> None:
        self._conn.close()

    @property
    def autocommit(self) -> bool:
        return self._conn.isolation_level is None

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        # SQLite uses isolation_level for transaction control
        # None = autocommit, "" or "DEFERRED" = manual transactions
        self._conn.isolation_level = None if value else ""

    def _ensure_cursor(self) -> Any:
        if self._cursor is None:
            self._cursor = self._conn.cursor()
        return self._cursor

    @staticmethod
    def _convert_params(sql: str, params: Any) -> tuple[str, Any]:
        """Convert PostgreSQL %(...)s params to SQLite ? params.

        Also handles RETURNING clause removal for SQLite.
        """
        import re
        # Remove RETURNING clause (SQLite doesn't support it the same way)
        sql = re.sub(r'\s+returning\s+[^;]+', '', sql, flags=re.IGNORECASE).strip()

        # Convert %(name)s to ? (positional)
        param_names = re.findall(r'%\((\w+)\)s', sql)
        sql = re.sub(r'%\(\w+\)s', '?', sql)

        # Handle dict params (single param that is a dict)
        if isinstance(params, dict):
            ordered_params = []
            for name in param_names:
                if name in params:
                    ordered_params.append(params[name])
                else:
                    ordered_params.append(None)
            return sql, tuple(ordered_params)

        # Handle list of dicts (for executemany)
        if isinstance(params, list) and params and isinstance(params[0], dict):
            converted = []
            for param_dict in params:
                ordered = []
                for name in param_names:
                    if name in param_dict:
                        ordered.append(param_dict[name])
                    else:
                        ordered.append(None)
                converted.append(tuple(ordered))
            return sql, converted

        return sql, params

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> None:
        """Execute a single statement."""
        cur = self._ensure_cursor()
        if params:
            sql, params = self._convert_params(sql, params)
        # Handle END; statements (from trigger definitions) by wrapping them
        # in a no-op SELECT to prevent SQLite from interpreting them as transactions
        if sql.strip() == 'END':
            cur.execute('SELECT 1')
            return
        cur.execute(sql, params or ())

    def fetchone(self, sql: str | None = None, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        cur = self._ensure_cursor()
        if sql is not None:
            if params:
                sql, params = self._convert_params(sql, params)
            cur.execute(sql, params or ())
        row = cur.fetchone()
        if row is None:
            return None
        keys = [d[0] for d in cur.description] if cur.description else []
        return dict(zip(keys, row))

    def fetchall(self, sql: str | None = None, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        cur = self._ensure_cursor()
        if sql is not None:
            if params:
                sql, params = self._convert_params(sql, params)
            cur.execute(sql, params or ())
        rows = cur.fetchall()
        if not rows:
            return []
        keys = [d[0] for d in cur.description] if cur.description else []
        return [dict(zip(keys, row)) for row in rows]

    def commit(self) -> None:
        if self._conn.in_transaction:
            self._conn.commit()

    def rollback(self) -> None:
        if self._conn.in_transaction:
            self._conn.rollback()

    def executemany(self, sql: str, params_list: list[tuple[Any, ...]]) -> None:
        """Execute a statement against multiple parameter sets."""
        cur = self._ensure_cursor()
        # Convert each param set and track the converted SQL
        converted = []
        converted_sql = sql
        for params in params_list:
            if params:
                converted_sql, c_params = self._convert_params(sql, params)
                converted.append(c_params)
            else:
                converted.append(params)
        cur.executemany(converted_sql, converted)

    def cursor(self) -> Any:
        """Return a cursor for direct SQL execution."""
        return self._ensure_cursor()

    def lastrowid(self) -> int:
        """Return the row id of the last inserted row."""
        return self._conn.lastrowid


class Connection:
    """A managed PostgreSQL connection.

    The connection is created on first access and closed either explicitly
    with :meth:`close` or by garbage collection. It is not safe to use after
    ``close`` has been called.
    """

    __slots__ = ("_dsn", "_conn", "_closed", "_config", "_connect_timeout")

    def __init__(self, config: DatabaseConfig, connect_timeout: int = 5) -> None:
        self._dsn = config.dsn
        self._conn: psycopg.Connection[dict[str, Any]] | None = None
        self._closed = False
        self._config = config
        self._connect_timeout = connect_timeout

    @property
    def config(self) -> DatabaseConfig:
        return self._config

    @property
    def closed(self) -> bool:
        return self._closed

    def _open(self) -> None:
        if self._closed:
            raise DatabaseConnectionError("connection has been closed")
        if self._conn is None:
            self._conn = _connect(self._dsn, self._connect_timeout)

    def close(self) -> None:
        if self._conn is not None and not self._closed:
            self._conn.close()
            self._conn = None
            self._closed = True

    def __enter__(self) -> "Connection":
        self._open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> "Connection":
        self._open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> None:
        """Execute a statement with parameters.

        The caller is responsible for commit/rollback.

        For SQLite, splits multi-statement SQL into individual executions
        since sqlite3 only allows one statement per execute() call.
        """
        self._open()
        if isinstance(self._conn, _SQLiteAdapter):
            # SQLite: split by semicolons and execute each statement
            import re
            statements = re.split(r';(?=\s*\n|\s*$)', sql)
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt:
                    continue
                # Skip pure comment lines but preserve statements that contain
                # both comments and SQL (comments are stripped, SQL is executed)
                # Remove inline comments for execution
                lines = stmt.split('\n')
                sql_lines = [l for l in lines if not l.strip().startswith('--')]
                clean_sql = '\n'.join(sql_lines).strip()
                if not clean_sql:
                    continue
                self._conn.execute(clean_sql, params or ())
        else:
            self._conn.execute(sql, params or ())

    def fetchone(self, sql: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        """Execute a query and return the first row as a dict."""
        self._open()
        return self._conn.fetchone(sql, params or ())

    def fetchall(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        """Execute a query and return all rows as dicts."""
        self._open()
        return self._conn.fetchall(sql, params or ())

    @property
    def autocommit(self) -> bool:
        self._open()
        return self._conn.autocommit

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        self._open()
        self._conn.autocommit = bool(value)


def get_connection() -> Connection:
    """Return a new Connection to the configured database.

    Reads AGENTOS_DB_PATH (SQLite) or DATABASE_URL (PostgreSQL) from the
    environment and returns an open Connection instance.
    """
    config = DatabaseConfig.from_env()
    return Connection(config)


def _connect(dsn: str, connect_timeout: int) -> Any:
    """Create a connection, failing clearly on failure.

    Supports PostgreSQL (psycopg 3, psycopg2) and SQLite backends.
    SQLite DSNs are identified by the ``sqlite:///`` prefix.
    """
    # SQLite fast path
    if dsn.startswith("sqlite:///"):
        import sqlite3 as _sqlite3
        db_path = dsn[len("sqlite:///"):]
        conn = _sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = _sqlite3.Row
        return _SQLiteAdapter(conn)

    # PostgreSQL path — psycopg3 preferred, psycopg2 fallback
    driver = _choose_driver()
    is_psycopg3 = hasattr(driver, "rows") and hasattr(driver.rows, "dict_row")
    try:
        if is_psycopg3:
            return driver.connect(dsn, connect_timeout=connect_timeout, row_factory=driver.rows.dict_row)
        # psycopg2 fallback — wrap to provide psycopg3-compatible API
        import psycopg2.extras  # type: ignore[import-not-found]
        conn = driver.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)
        return _Psycopg2Adapter(conn)
    except (AttributeError, TypeError) as exc:
        if "rows" in str(exc).lower():
            raise UnknownDatabaseDriver(
                "psycopg2 detected but code expects psycopg3 API; "
                "install psycopg>=3 for full support"
            ) from exc
        raise
    except Exception as exc:
        if hasattr(driver, "OperationalError") and isinstance(exc, driver.OperationalError):
            _raise_connection_error(dsn, exc)
        elif hasattr(driver, "Error") and isinstance(exc, driver.Error):
            raise DatabaseConnectionError(_message_from_error(exc)) from exc
        raise


def _choose_driver() -> Any:
    """Pick the running psycopg driver. Supports psycopg 3 and psycopg 2."""
    # Check module-level binding set by a prior import; safe for unbound name
    for name, mod in list(globals().items()):
        if name == "psycopg" and isinstance(mod, type(__import__("types").ModuleType)) and hasattr(mod, "connect"):
            return mod
    try:
        import psycopg  # psycopg 3
        globals()["psycopg"] = psycopg
        return psycopg
    except ImportError as exc:
        try:
            import psycopg2 as psycopg  # type: ignore[no-redef]
        except ImportError as exc2:
            raise UnknownDatabaseDriver(
                "no supported PostgreSQL driver found: install psycopg>=3 "
                "(psycopg[binary] recommended)"
            ) from exc2
        globals()["psycopg"] = psycopg
        return psycopg
    return psycopg


def _message_from_error(exc: BaseException) -> str:
    """Render a concise error message from a database exception."""
    if exc is None:
        return "database error"
    exc_type = type(exc).__name__
    text = str(exc).strip() if str(exc) else "database error"
    return f"{exc_type}: {text}"


def _raise_connection_error(dsn: str, exc: BaseException) -> None:
    """Convert a psycopg OperationalError into a typed, diagnosable failure."""
    host, port = _dsn_hostport(dsn)
    hint = ""
    if isinstance(exc, (psycopg.OperationalError,)):
        if "connection refused" in str(exc).lower():
            hint = (
                f"connection refused to {host}:{port}; ensure PostgreSQL is running "
                f"and accepting connections at that host and port"
            )
        elif "timeout" in str(exc).lower():
            hint = f"connection to {host}:{port} timed out"
        elif "authentication" in str(exc).lower() or "password" in str(exc).lower():
            hint = "authentication failed; check DATABASE_URL credentials"
    message = " ".join(s for s in [str(exc).strip(), hint if hint else "", ""] if s)
    message = message or f"cannot connect to PostgreSQL at {host}:{port}"
    raise DatabaseConnectionError(message) from exc


def _dsn_hostport(dsn: str) -> tuple[str, int]:
    try:
        parts = _parse_dsn(dsn)
        return parts["host"], parts["port"]
    except DatabaseConnectionError:
        return "unknown", 5432


class Session(AbstractContextManager):
    """A transactional database session.

    Opens a connection, disables autocommit, and commits on successful exit
    or rolls back on any exception. The inner ``connection`` may be used for
    additional queries inside the transaction.
    """

    __slots__ = ("_connection",)

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def __enter__(self) -> Connection:
        connection = self._connection
        connection._open()
        connection._conn.autocommit = False
        return connection._conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        connection = self._connection._conn
        if connection is None:
            return False
        try:
            if exc_type is None:
                connection.commit()
            else:
                connection.rollback()
        except Exception as exc:
            try:
                connection.rollback()
            except Exception:
                pass
            raise DatabaseError(_message_from_error(exc)) from exc
        return False


async def async_connection(config: DatabaseConfig, connect_timeout: int = 5) -> AsyncIterator[psycopg.AsyncConnection[dict[str, Any]]]:
    """Contextual async connection to the configured database."""
    driver = _choose_driver()
    if not hasattr(driver, "connect_async"):
        raise UnknownDatabaseDriver("async connections require psycopg>=3")
    conn = await driver.connect_async(config.dsn, connect_timeout=connect_timeout, row_factory=psycopg.rows.dict_row)
    try:
        yield conn
    finally:
        await conn.close()
