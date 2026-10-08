"""Append-only event store backed by PostgreSQL.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable

import psycopg

from .config import DatabaseConfig
from .connection import Connection, Session, async_connection
from .errors import (
    DatabaseConnectionError,
    DatabaseError,
    EventDuplicateError,
    EventImmutableError,
    EventValidationError,
    MigrationError,
)
from .migrations import run as _run_migrations
from .models import DEFAULT_PAYLOAD_SCHEMA, Event, event_from_dict


class EventStore:
    """Generic append-only event store.

    All mutations happen inside explicit transactions. An ``append`` that
    fails at any point rolls back the whole batch, so history is never
    partially persisted.
    """

    __slots__ = ("_connection", "_config")

    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        if isinstance(connection, DatabaseConfig):
            self._config = connection
            self._connection = Connection(connection)
        else:
            self._connection = connection
            self._config = connection.config

    @classmethod
    def from_config(cls, config: DatabaseConfig) -> "EventStore":
        """Build an event store from a :class:`DatabaseConfig`."""
        return cls(config)

    @classmethod
    def apply_migrations(cls, config: DatabaseConfig) -> list[str]:
        """Run pending database migrations for this store.

        Migrations are applied idempotently: re-running on an already
        migrated database is a no-op and leaves the schema unchanged.
        """
        return _run_migrations(config)

    def append(self, events: Iterable[Event]) -> list[Event]:
        """Insert one or more events inside a single transaction.

        All events are validated first, then inserted in one transaction so
        that a failure rolls back everything: no event from a failed batch is
        persisted. On success the returned events carry the database-generated
        ``version`` and (when ``id`` was DB-generated) the ``id`` set.
        """
        events = tuple(events)
        if not events:
            return []

        seen_ids: dict[Event, str] = {}
        validated: list[Event] = []
        for event in events:
            normalized = event.normalize_for_insert()
            try:
                _validate_event(normalized)
            except EventValidationError as exc:
                raise exc
            if event.id is not None:
                hex_id = _hex_id(event.id)
                if hex_id in seen_ids:
                    raise EventValidationError(
                        f"duplicate event id {event.id} within the same append"
                    )
                seen_ids[normalized] = hex_id
            validated.append(normalized)

        sql = """
            insert into event_store
                (id, occurred_at, aggregate_type, aggregate_id, event_type,
                 payload, payload_schema, version, source)
            values
                (%(id)s, %(occurred_at)s, %(aggregate_type)s, %(aggregate_id)s,
                 %(event_type)s, %(payload)s, %(payload_schema)s, %(version)s, %(source)s)
            returning id, occurred_at, aggregate_type, aggregate_id, event_type,
                      payload, payload_schema, version, source
        """
        with Session(self._connection) as cursor:
            rows: list[dict] = []
            for event in validated:
                row: dict = {
                    "id": _hex_id(event.id),
                    "occurred_at": _serialize_timestamp(event.occurred_at),
                    "aggregate_type": event.aggregate_type,
                    "aggregate_id": _hex_id(event.aggregate_id),
                    "event_type": event.event_type,
                    "payload": _serialize_payload(event.payload),
                    "payload_schema": event.payload_schema,
                    "version": event.version,
                    "source": event.source,
                }
                rows.append(row)
            cursor.executemany(sql, rows)
            rows = [dict(row) for row in cursor.fetchall()]
        return [_row_to_event(row, seen_ids) for row in rows]

    def get(self, event_id: str | uuid.UUID) -> Event | None:
        """Fetch a single event by id."""
        with Session(self._connection) as cursor:
            cursor.execute(
                "select id, occurred_at, aggregate_type, aggregate_id, event_type,"
                " payload, payload_schema, version, source from event_store"
                " where id = %s",
                (_hex_id(event_id),),
            )
            row = cursor.fetchone()
            return _row_to_event(row, {}) if row else None

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str | uuid.UUID) -> list[Event]:
        """Fetch all events for an aggregate, ordered by version (deterministic)."""
        with Session(self._connection) as cursor:
            cursor.execute(
                "select id, occurred_at, aggregate_type, aggregate_id, event_type,"
                " payload, payload_schema, version, source from event_store"
                " where aggregate_type = %s and aggregate_id = %s"
                " order by version",
                (aggregate_type, _hex_id(aggregate_id)),
            )
            rows = [dict(row) for row in cursor.fetchall()]
        return [_row_to_event(row, {}) for row in rows]

    def list_chronological(self, limit: int = 100) -> list[Event]:
        """Fetch the most recent events in deterministic order."""
        with Session(self._connection) as cursor:
            cursor.execute(
                "select id, occurred_at, aggregate_type, aggregate_id, event_type,"
                " payload, payload_schema, version, source from event_store"
                " order by version desc, occurred_at desc limit %s",
                (limit,),
            )
            rows = [dict(row) for row in cursor.fetchall()]
        return [_row_to_event(row, {}) for row in rows]

    def exists(self, event_id: str | uuid.UUID) -> bool:
        """Check whether an event with the given id exists."""
        with Session(self._connection) as cursor:
            cursor.execute(
                "select 1 from event_store where id = %s limit 1",
                (_hex_id(event_id),),
            )
            return cursor.fetchone() is not None

    def count(self) -> int:
        """Return the total number of persisted events."""
        with Session(self._connection) as cursor:
            cursor.execute("select count(*) as n from event_store")
            row = cursor.fetchone()
            return row["n"] if row else 0


def _row_to_event(row: dict, seen_ids: dict[Event, str]) -> Event:
    """Convert a database row into an :class:`Event`."""
    data: dict = {
        "id": uuid.UUID(hex=row["id"]),
        "occurred_at": _deserialize_timestamp(row["occurred_at"]),
        "aggregate_type": row["aggregate_type"],
        "aggregate_id": uuid.UUID(hex=row["aggregate_id"]),
        "event_type": row["event_type"],
        "payload": _deserialize_payload(row["payload"]),
        "payload_schema": row["payload_schema"],
        "version": int(row["version"]) if row["version"] is not None else None,
        "source": row.get("source"),
    }
    return Event.model_validate(data)


def _validate_event(event: Event) -> None:
    """Application-level validation of an event before insertion."""
    if not event.event_type:
        raise EventValidationError("event_type is required")
    if not event.aggregate_type:
        raise EventValidationError("aggregate_type is required")
    if not event.aggregate_id:
        raise EventValidationError("aggregate_id is required")
    if event.occurred_at is None:
        raise EventValidationError("occurred_at is required")
    if event.payload_schema is None or not event.payload_schema.strip():
        raise EventValidationError("payload_schema is required")
    if len(event.payload_schema) > 63:
        raise EventValidationError("payload_schema too long (max 63 characters)")
    if not isinstance(event.payload, dict):
        raise EventValidationError("payload must be a JSON-serializable object")
    try:
        _serialize_payload(event.payload)
    except (TypeError, ValueError) as exc:
        raise EventValidationError(f"payload is not serializable: {exc}") from exc


def _serialize_timestamp(ts: datetime) -> str:
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=datetime.timezone.utc)
    return ts.isoformat()


def _deserialize_timestamp(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def _serialize_payload(payload: dict) -> str:
    return Event.model_validate({"payload": payload}).model_dump_json()


def _deserialize_payload(value: str | dict) -> dict:
    if isinstance(value, dict):
        return value
    return Event.model_validate({"payload": value}).model_dump()["payload"]


def _hex_id(identifier: str | uuid.UUID) -> str:
    if isinstance(identifier, uuid.UUID):
        return identifier.hex
    return identifier
