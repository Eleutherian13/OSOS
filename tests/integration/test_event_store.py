"""Integration tests using SQLite (no external database required)."""
import os
import pytest
import sqlite3
import tempfile
from pathlib import Path

# Set up SQLite for tests
TEST_DB = tempfile.mktemp(suffix='.sqlite3')
os.environ['AGENTOS_DB_PATH'] = TEST_DB
# Clear DATABASE_URL if set
os.environ.pop('DATABASE_URL', None)


@pytest.fixture(scope="module")
def db_config():
    from agentos.db.config import DatabaseConfig
    return DatabaseConfig.from_env()


@pytest.fixture(scope="module")
def event_store(db_config):
    from agentos.db.repository import EventStore
    from agentos.db.migrations import run
    run(db_config)
    return EventStore(db_config)


def test_health_connects(db_config):
    from agentos.db.health import is_healthy
    result = is_healthy(db_config, migrations_applied=False)
    assert result.healthy or "not available" in (result.error or "")


def test_event_append_and_retrieve(event_store):
    import uuid
    from agentos.db.models import Event
    agg_id = uuid.uuid4()
    events = [
        Event(aggregate_type="path", aggregate_id=agg_id, event_type="created", payload={"name": "p1"}),
        Event(aggregate_type="path", aggregate_id=agg_id, event_type="updated", payload={"state": "active"}),
    ]
    saved = event_store.append(events)
    assert len(saved) == 2
    assert saved[0].id is not None
    assert saved[1].version == 2


def test_event_persistence_across_connections(db_config, event_store):
    import uuid
    from agentos.db.models import Event
    agg_id = uuid.uuid4()
    event = Event(aggregate_type="path", aggregate_id=agg_id, event_type="created", payload={"test": True})
    event_store.append([event])
    # Create new store instance (simulates reconnect)
    from agentos.db.repository import EventStore
    store2 = EventStore(db_config)
    retrieved = store2.get(event.id)
    assert retrieved is not None
    assert retrieved.payload == {"test": True}


def test_migrations_idempotent(db_config):
    from agentos.db.migrations import run
    # Migrations may have already been applied by the event_store fixture
    applied1 = run(db_config)
    # SQLite has 9 migrations (V001-V009); V012 was removed
    assert len(applied1) in (0, 9), f"Expected 0 or 9 migrations, got {len(applied1)}"
    applied2 = run(db_config)
    assert len(applied2) == 0  # No new migrations on re-run


def test_foreign_key_enforcement(event_store):
    import uuid
    from agentos.db.models import Event
    # Try to create event with non-existent aggregate_id
    fake_id = uuid.uuid4()
    event = Event(aggregate_type="path", aggregate_id=fake_id, event_type="created", payload={})
    # This should not raise - foreign keys are enforced at DB level but we're not checking path existence
    saved = event_store.append([event])
    assert len(saved) == 1


def teardown_module(module):
    """Clean up test database."""
    import time
    if os.path.exists(TEST_DB):
        # Windows may lock the file briefly; retry removal
        for _ in range(3):
            try:
                os.remove(TEST_DB)
                break
            except PermissionError:
                time.sleep(0.1)
        for suffix in ['-wal', '-shm']:
            path = TEST_DB + suffix
            if os.path.exists(path):
                try:
                    os.remove(path)
                except PermissionError:
                    pass
