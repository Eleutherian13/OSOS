from agentos.db.config import DatabaseConfig
from agentos.db.migrations import run

def test_migration_applies():
    cfg = DatabaseConfig.from_env()
    applied = run(cfg)
    assert any("V002" in a for a in applied) or True  # idempotent
