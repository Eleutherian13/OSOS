"""Database error types surfaced by the AgentOS persistence layer.

All exceptions carry the underlying database exception as ``__cause__`` so the
original cause remains inspectable (connection failure, constraint failure,
transaction failure, serialization failure).
"""

from typing import Any


class AgentOSDatabaseError(Exception):
    """Base class for all AgentOS database errors."""


class DatabaseConnectionError(AgentOSDatabaseError):
    """Failed to establish a connection to PostgreSQL."""


class DatabaseError(AgentOSDatabaseError):
    """A database operation failed."""


class EventValidationError(AgentOSDatabaseError):
    """An event failed application-level validation."""


class EventDuplicateError(AgentOSDatabaseError):
    """A duplicate event identity was rejected."""


class EventImmutableError(AgentOSDatabaseError):
    """An attempt to update or delete an event was rejected by the database."""


class MigrationError(AgentOSDatabaseError):
    """A database migration failed to run."""


class UnknownDatabaseDriver(AgentOSDatabaseError):
    """The configured PostgreSQL driver is not supported."""


def _message_from_error(exc: BaseException) -> str:
    """Render a concise, non-sensitive error message from a database exception."""
    if exc is None:
        return "database error"
    exc_type = type(exc).__name__
    text = str(exc).strip() if str(exc) else "database error"
    return f"{exc_type}: {text}"
