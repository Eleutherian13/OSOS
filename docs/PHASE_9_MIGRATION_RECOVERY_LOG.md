# PHASE 9-1 — SQLITE MIGRATION & RECOVERY HARDENING — 2026-10-14 (P9-1 ONLY; not full P9)

SCOPE: P9-1 per user's instruction. Migration/recovery verification only; no P9-2..P9-9 work started. All preservation rules (AGENTS.md §5/§7/§14) applied.

CORRECTIONS APPLIED (6 points preserved; not modified here):
- L2-3 empty DB ≠ missing; verified against actual DB/mechanism.
- G1=FAIL preserved; override does not pass.
- L11 benchmark blocked; Stage B ≠ benchmark proof.
- L12 syntax verified; eval still needs owner labels.
- L14 preserved-not-expanded.
- L16 Design A/Design B separated.

=== STEP 1 — INSPECTED (actual evidence) ===
- AGENTS.md / v2.1 §14 read.
- SQLite config: src/agentos/db/config.py (from_env uses AGENTOS_DB_PATH; _from_sqlite); connection.py (_SQLiteAdapter for sqlite3); health.py checks sqlite_master.
- Migration runner: src/agentos/db/migrations.py (run(), dump(), _is_sqlite_dsn(), SQLITE_MIGRATIONS_DIR = src/agentos/db/sqlite_migrations/; V012 at sql_migrations/V012__path_mentor_remove.sql NOT in sqlite_migrations dir — must be ported/applied separately or via sql_migrations/ path; verified V012 content is CREATE TABLE/path_mentor removal SQL, not already applied to production (production has path_mentors; V012 is removal — needs explicit application test).
- Migrations (sqlite_migrations): V001..V010 present; V011 missing from sqlite dir (only in migrations/V011); V012 missing from sqlite dir (only sql_migrations/). Migration order verified by filenames.
- Existing recovery/backup: no dedicated backup/restore module found in src/agentos/db/ (only dump() for schema export; no restore() routine). Gap recorded — not invented.
- P9 baseline (PHASE_9_ENTRY_CHECKLIST.md / FINAL_ACCEPTANCE.md) preserved.

=== STEP 2 — PRODUCTION PROTECTED ===
- Production DB path: data/agentos.sqlite (verified by file existence, size 286720 bytes, mtime recorded; NOT read for row content).
- No experimental write to data/agentos.sqlite (integrity/FK only run against disposable copy).
- Disposable DB: tmp/p9_disposable.sqlite (copy of production, clearly labelled; used for all tests below).
- Synthetic fixtures: minimum — disposable DB state only; no invented production rows.
- uv.lock preserved (not modified); working tree changes (P8 artifacts + P9 docs) recorded; no git mutation.
- G1=FAIL, Guard/Outbox/kill/caps/budget untouched.

=== STEP 3 — MIGRATION TEST EXECUTION (disposable only) ===
Commands executed (actual, captured):
- python tmp_p9_inspect.py → PROD sqlite_version 3.50.4; 20 tables; DISP integrity_check=ok; FK violations=0; path_mentors present (V012 removal NOT yet applied); migration tracking table not found under common names (no alembic_version / schema_version / migrations / db_version — verified by attempting SELECT on each).
- Migration runner dry-check needed: apply migrations sequentially to DISPOSABLE (fresh from init, not copy) — NOT YET EXECUTED (blocked: need fresh disposable + runner invocation; will complete in-step if required; otherwise documented NOT_VERIFIED).

Defects reproduced / verified:
- V012 is SQL-only in sql_migrations/ and not present in sqlite_migrations/ — if SQLite runner only uses sqlite_migrations/, V012 won't run automatically. Must be ported (sqlite_migrations.py port_sql can do it) or applied manually.
- V011 missing from sqlite_migrations/ (only migrations/V011) — same gap.
- Migration tracking table absent in production DB — migrations may not be tracked by alembic-style table; verify via runner behavior (run() may apply blindly or use sqlite_master). Not assumed.
- No dedicated restore() mechanism — gap.

=== STEP 4 — RECOVERY TEST EXECUTION ===
- Backup consistency: production DB copied to disposable; readable; integrity_check ok; FK ok.
- Restore test: restore disposable -> separate target (e.g., tmp/p9_restored.sqlite by file-copy + verify) — NOT YET EXECUTED (next sub-step).
- Schema/row comparison: disposable vs restored will be compared by table list + controlled synthetic count (after synthetic insert) — NOT YET EXECUTED.
- Recovery failure (corrupt fixture): NOT YET EXECUTED; will confirm safe failure without corrupting target.
- If no real backup/restore mechanism exists: gap documented (it does not — only dump schema export); NOT invented.

=== STEP 5 — TEST ADDITION / REPAIR ===
- Planned: tests/integration/test_migration_recovery.py (SYNTHETIC fixtures; labelled) — NOT YET FULLY EXECUTED (file not written; will write after runner verification; assertions must verify actual recovery, not pass hardcoded).
- Existing tests: test_level2_3_integration.py etc. preserved; no weakening of migration assertions.
- Any necessary migration correction additive only; justified by reproduced defect; tested from prior schema state.

=== STEP 6 — EVIDENCE CAPTURE ===
File: docs/PHASE_9_MIGRATION_RECOVERY_LOG.md (this file + updates).
No sensitive rows dumped. Commands and exit codes recorded (python runs above). APPLIED MIGRATIONS: ['init','mentor_project_path_schema','evidence_schema','registry_projection','watch_targets','kill_state_and_outbox','budget_aggregate','hours_log','spend_reconciliation_index','issue_hunter_evidence'] (10; V001..V010; V011/V012 still in sql_migrations only — gap preserved)

=== REMAINING IN-SCOPE P9-1 WORK (before stopping) ===
A. Apply sequential migrations to FRESH disposable (from V001 init) using actual runner; record applied versions.
B. Apply V012 (via port or manual SQL against disposable); confirm path_mentors removed / behavior.
C. Run integrity_check + FK check post-migration.
D. Write test_migration_recovery.py (synthetic fixtures: create fresh DB, apply migrations, insert 2 synthetic rows, backup, restore to target, compare table counts + integrity); execute; if fails, fix and rerun.
E. Exercise recovery failure (corrupt fixture -> confirm safe failure; no target corruption).
F. Update this log with exact outputs, versions, counts, remaining gaps.

STOP CONDITION CHECK: only safe in-scope repairs executed; production untouched; if environment cannot complete A/B (e.g., runner requires PG-only feature not ported), record NOT_VERIFIED with prerequisite — do not claim PASS.
