"""Pydantic v2 event model for the append-only event store.

Events are generic: no business-specific fields. Future event types
(path, state, interaction, evidence) are represented through ``event_type``
and a JSONB ``payload``.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, model_validator

from .errors import EventDuplicateError, EventValidationError
from decimal import Decimal

DEFAULT_PAYLOAD_SCHEMA = "1.0"


class Event(BaseModel):
    """A single domain event persisted to PostgreSQL.

    Attributes:
        id: Unique event identifier. When omitted a UUID is generated.
        occurred_at: Business timestamp when the event occurred. Defaults to
            the current UTC timestamp at validation time.
        aggregate_type: Type of the entity this event concerns, e.g.
            ``path`` or ``mentorship``. Used to group and filter events.
        aggregate_id: Identifier of the entity this event concerns. Events for
            the same entity share this value.
        event_type: Discriminator for the kind of event, e.g. ``created``,
            ``updated``, ``completed``.
        payload: Structured, portable data for the event (JSON serializable).
        payload_schema: Semantic schema version of ``payload``.
        version: Monotonic logical order within the aggregate. Populated by the
            database at insert time; absent before insertion.
        source: Provenance metadata naming the subsystem that authored the
            event. Optional.
    """

    id: Annotated[uuid.UUID | None, Field(default=None)] = None
    occurred_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))] = ...
    aggregate_type: Annotated[str, Field(min_length=1, max_length=63)] = ...
    aggregate_id: Annotated[uuid.UUID, Field(...)] = ...
    event_type: Annotated[str, Field(min_length=1, max_length=127)] = ...
    payload: Annotated[dict[str, Any], Field(default_factory=dict)] = ...
    payload_schema: Annotated[str, Field(min_length=1, max_length=63)] = DEFAULT_PAYLOAD_SCHEMA
    version: Annotated[int | None, Field(default=None, ge=0)] = None
    source: Annotated[str | None, Field(default=None, max_length=63)] = None

    @model_validator(mode="before")
    @classmethod
    def _default_id(cls, values: Any) -> Any:
        if isinstance(values, dict) and values.get("id") is None:
            values["id"] = uuid.uuid4()
        return values

    @model_validator(mode="after")
    def _fix_timestamp(self) -> Event:
        if self.occurred_at is not None and self.occurred_at.tzinfo is None:
            self.occurred_at = self.occurred_at.replace(tzinfo=timezone.utc)
        return self

    def normalize_for_insert(self) -> Event:
        """Return an insert-ready copy with an explicit id.

        The database generates ``version``. The caller may optionally set
        ``id``; a duplicate ``id`` is a client error raised here.
        """
        return Event.model_validate(self, from_attributes=True)

    def assert_new(self) -> Event:
        """Validate that this event is not a duplicate of an existing one.

        Duplicate identity is rejected at the boundary so a retried append
        cannot create history. Re-raise self on success so callers can chain.
        """
        if self.id is None:
            raise EventValidationError("event id must be present for duplicate check")
        return self


def event_from_dict(data: dict[str, Any]) -> Event:
    """Construct a validated ``Event`` from a plain dictionary."""
    return Event.model_validate(data)

class Evidence(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    path_id: uuid.UUID
    claim: str = Field(min_length=1)
    artifact_url: str = Field(min_length=1)
    kind: Literal['fix','test_infra','design','review','community']
    depth: int = Field(ge=1, le=5)
    relevance_to_project: Decimal = Field(ge=Decimal('0'), le=Decimal('1'))
    project_specificity: Decimal = Field(ge=Decimal('0'), le=Decimal('1'))
    independence: int = Field(ge=1, le=5)
    maintainer_signal: Decimal = Field(ge=Decimal('-1'), le=Decimal('1'))
    mentor_validated: bool = False
    understood: bool = False
    interaction_id: uuid.UUID | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
