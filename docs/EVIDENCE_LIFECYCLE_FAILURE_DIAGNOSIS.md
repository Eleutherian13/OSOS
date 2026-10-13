# Evidence Lifecycle Failure Diagnosis
Status: TEST_ASSUMPTION — CONFIRMED
Root cause: test_evidence_lifecycle (tests/integration/test_evidence_db.py:9-24) uses hardcoded DSN postgresql://localhost:5432/postgres; project uses SQLite (AGENTS.md §5).
Not repaired — outside verification-only scope (would require PostgreSQL service or test rewrite / persistence change).
Preservation: DB/V012/uv.lock/G1 unchanged; no source edit.
