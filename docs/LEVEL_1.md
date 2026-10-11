# Level 1 — Persistence Contract (Summary)

- PostgreSQL 16+ event store (`migrations/V001__init.sql`)
- Generic `Event` (Pydantic v2) with DB-level immutability (trigger + grants)
- Migration registry (`db_migrations`) guarantees idempotency
- `EventStore.append/get/list_by_aggregate` transaction-safe
- Config via `DATABASE_URL` only; secrets not committed
- Integration tests use real PostgreSQL (skipped cleanly when unavailable)
- Level 2 NOT implemented

Full details: `docs/LEVEL_1_REPORT.md`
