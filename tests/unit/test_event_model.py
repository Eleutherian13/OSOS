"""Unit tests for agentos.db.models (no PostgreSQL required)."""

import uuid
import pytest
from agentos.db.models import Event, event_from_dict


def test_event_valid() -> None:
    from uuid import uuid4
    e = Event(aggregate_type="t", aggregate_id=uuid4(), event_type="x")
    assert e.event_type == "x"
    assert e.id is not None


def test_event_missing_aggregate() -> None:
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        Event(event_type="x")
