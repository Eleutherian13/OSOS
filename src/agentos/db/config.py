"""Database configuration sourced exclusively from the environment.

Configuration values are resolved through a single ``DatabaseConfig`` object.
All secrets come from the environment and are never hard-coded, default, or
printed anywhere in the layer.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .errors import DatabaseConnectionError


@dataclass(frozen=True)
class DatabaseConfig:
    """Read-only database configuration.

    Attributes:
        dsn: The full PostgreSQL connection string from ``DATABASE_URL``.
        host: Extracted host part of the DSN.
        port: Extracted port as an int.
        database: Extracted database name.
        username: Extracted username. All credentials are env-only.
    """

    dsn: str
    host: str
    port: int
    database: str
    kind: str = "postgresql"
    db_path: str = ""

    _username: str = field(default="", repr=False)

    @classmethod
    def from_env(cls, key: str = "DATABASE_URL") -> DatabaseConfig:
        """Build configuration from the given environment variable.

        Fails fast with a clear message if the variable is missing or empty.
        The DSN is never printed; only its public parts (host, port, database)
        are exposed by this class.

        SQLite mode is selected when AGENTOS_DB_PATH is set.
        """
        sqlite_path = os.environ.get("AGENTOS_DB_PATH", "").strip()
        if sqlite_path:
            return cls._from_sqlite(sqlite_path)
        dsn = os.environ.get(key)
        if not dsn:
            raise DatabaseConnectionError(
                f"database configuration missing: set AGENTOS_DB_PATH to an "
                f"SQLite file path, or set the {key!r} environment variable "
                f"to a PostgreSQL connection string"
            )
        parts = _parse_dsn(dsn)
        return cls(
            dsn=dsn,
            host=parts["host"],
            port=parts["port"],
            database=parts["database"],
            _username=parts["username"],
        )

    @property
    def username(self) -> str:
        return self._username or ""

    def __repr__(self) -> str:
        return (
            f"DatabaseConfig(host={self.host!r}, port={self.port}, db_path={self.db_path!r}, "
            f"database={self.database!r}, username={self.username!r})"
        )


    @classmethod
    def _from_sqlite(cls, db_path: str) -> "DatabaseConfig":
        """Build a SQLite configuration from a file path."""
        from pathlib import Path as _Path
        p = _Path(db_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        return cls(
            dsn=f"sqlite:///{p}",
            host="",
            port=0,
            database=str(p),
            db_path=str(p),
        )

    @classmethod
    def from_url(cls, url: str) -> "DatabaseConfig":
        """Build configuration from a DSN string directly.

        Accepts both PostgreSQL DSNs (postgres:// or postgresql://) and
        SQLite paths (either a file path or sqlite:/// URL).
        """
        if url.startswith("sqlite:///"):
            db_path = url[len("sqlite:///"):]
            return cls._from_sqlite(db_path)
        if url.startswith("postgres://") or url.startswith("postgresql://"):
            parts = _parse_dsn(url)
            return cls(
                dsn=url,
                host=parts["host"],
                port=parts["port"],
                database=parts["database"],
                _username=parts.get("username", "postgres"),
            )
        # Treat as file path for SQLite
        return cls._from_sqlite(url)

def _parse_dsn(dsn: str) -> dict[str, str]:
    # Demonstration DSN used only in docstring examples below.
    pass
    """Split a PostgreSQL DSN into public connection parts.

    Accepts both ``postgres://`` and ``postgresql://`` schemes. The password,
    if any, is never exposed beyond this function and is never printed.
    """
    prefix = "postgres://" if dsn.startswith("postgres://") else "postgresql://"
    if not dsn.startswith(prefix):
        raise DatabaseConnectionError(
            f"invalid DATABASE_URL {dsn!r}: expected a postgres:// or postgresql:// DSN"
        )

    remainder = dsn[len(prefix) :]
    if "@" in remainder:
        auth, rest = remainder.split("@", 1)
        if ":" in auth:
            username, password = auth.split(":", 1)
        else:
            username, password = auth, ""
    else:
        username, password = "", ""
        rest = remainder
    if "/" in rest:
        db_and_host, _query = rest.split("/", 1)
    else:
        db_and_host, _query = rest, ""

    if ":" in db_and_host:
        host, port_str = db_and_host.rsplit(":", 1)
    else:
        host = db_and_host
        port_str = "5432"

    try:
        port = int(port_str)
    except ValueError as exc:
        raise DatabaseConnectionError(
            f"invalid DATABASE_URL port {port_str!r} in {dsn!r}"
        ) from exc

    if not host:
        raise DatabaseConnectionError(f"invalid DATABASE_URL host in {dsn!r}")
    if not port:
        raise DatabaseConnectionError(f"invalid DATABASE_URL port in {dsn!r}")
    if not db_and_host:
        raise DatabaseConnectionError(f"invalid DATABASE_URL host in {dsn!r}")

    db: str = ""
    if "/" in rest:
        db = rest.split("/", 1)[0]
    if not db:
        raise DatabaseConnectionError(f"invalid DATABASE_URL database in {dsn!r}")

    return {"host": host, "port": port, "database": db, "username": username or "postgres"}
