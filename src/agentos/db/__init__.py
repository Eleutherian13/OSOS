"""Event store: append-only persistence on PostgreSQL.

This package is the Level 1 persistence layer for AgentOS. It provides:

- :mod:`config` — database configuration from environment variables.
- :mod:`connection` — connection management and transactional sessions.
- :mod:`models` — the generic :class:`~agentos.db.models.Event` model.
- :mod:`repository` — the :class:`~agentos.db.repository.EventStore` API.
- :mod:`migrations` — the migration runner for SQL migrations.
- :mod:`health` — PostgreSQL connectivity health checks.
- :mod:`errors` — typed error classes.

Usage

    from agentos.db.config import DatabaseConfig
    from agentos.db.repository import EventStore

    config = DatabaseConfig.from_env()
    EventStore.apply_migrations(config)
    store = EventStore(config)
    event = store.append([Event(
        aggregate_type="path",
        aggregate_id=some_uuid,
        event_type="created",
        payload={"name": "my-path"},
    )])[0]

Events are generic: there are no domain-specific methods such as
``add_path_event``. Every future event type is persisted through the same
generic table. Immutability is enforced by a PostgreSQL trigger so events
cannot be updated or deleted from any client, including this application.
"""

from .config import DatabaseConfig
from .connection import Connection, Session, async_connection
from .errors import (
    AgentOSDatabaseError,
    DatabaseConnectionError,
    DatabaseError,
    EventDuplicateError,
    EventImmutableError,
    EventValidationError,
    MigrationError,
    UnknownDatabaseDriver,
)
from .health import HealthResult, is_healthy
from .migrations import MIGRATIONS_DIR, dump, run
from .models import DEFAULT_PAYLOAD_SCHEMA, Event, event_from_dict
from .repository import EventStore

__all__ = [
    "AgentOSDatabaseError",
    "DatabaseConnectionError",
    "DatabaseError",
    "EventDuplicateError",
    "EventImmutableError",
    "EventValidationError",
    "MigrationError",
    "UnknownDatabaseDriver",
    "DatabaseConfig",
    "Connection",
    "Session",
    "async_connection",
    "HealthResult",
    "is_healthy",
    "MIGRATIONS_DIR",
    "dump",
    "run",
    "Event",
    "event_from_dict",
    "DEFAULT_PAYLOAD_SCHEMA",
    "EventStore",
]
