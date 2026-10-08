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
        """
        self._open()
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


def _connect(dsn: str, connect_timeout: int) -> psycopg.Connection[dict[str, Any]]:
    """Create a psycopg connection, failing clearly on failure."""
    driver = _choose_driver()
    try:
        return driver.connect(dsn, connect_timeout=connect_timeout, row_factory=psycopg.rows.dict_row)
    except psycopg.OperationalError as exc:
        _raise_connection_error(dsn, exc)
    except psycopg.Error as exc:
        raise DatabaseConnectionError(_message_from_error(exc)) from exc
    raise UnknownDatabaseDriver(f"unrecognized psycopg connection failure")


def _choose_driver() -> Any:
    """Pick the running psycopg driver. Supports psycopg 3 and psycopg 2."""
    if "psycopg" in globals():
        return psycopg
    try:
        import psycopg  # psycopg 3
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
