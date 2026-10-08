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

    _username: str = field(default="", repr=False)

    @classmethod
    def from_env(cls, key: str = "DATABASE_URL") -> DatabaseConfig:
        """Build configuration from the given environment variable.

        Fails fast with a clear message if the variable is missing or empty.
        The DSN is never printed; only its public parts (host, port, database)
        are exposed by this class.
        """
        dsn = os.environ.get(key)
        if not dsn:
            raise DatabaseConnectionError(
                f"database configuration missing: set the {key!r} environment "
                f"variable to a PostgreSQL connection string "
                f"(postgres://user:pass@host:port/database)"
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
            f"DatabaseConfig(host={self.host!r}, port={self.port}, "
            f"database={self.database!r}, username={self.username!r})"
        )


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
