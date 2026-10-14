# PHASE 9-4 — INTEGRATED V0 CLI/SQLITE WORKFLOW REPLAY — 2026-10-14 (P9-4 ONLY)

SCOPE: P9-4 only; P9-1/2/3 done; P9-5+ not started; 6 corrections preserved; G1=FAIL/act=OFF/SQLite preserved.

=== 1. REAL WORKFLOW (derived from existing CLI / repos / tests / V002/V012 schema) ===
Canonical path from CLI + repository code (verified by source read, not invented):
- cli_path.py / cli_readiness.py / cli_next.py use DatabaseConfig.from_env() (AGENTOS_DB_PATH / DATABASE_URL).
- V002 (sqlite_migrations) defines paths/mentors/interactions/prerequisites; V003 evidence; V005 watch_targets; V006 kill/outbox; V010 issue_hunter.
- Path creation validates state ∈ (WATCH/ENGAGED/ACTIVE/BACKUP/DROPPED); mentor interaction logging writes interactions (email/issue/pr/meeting/other); evidence links to source locations; readiness reports 5-item checklist (lowest unmet first); watcher produces events/diffs; unchanged runs produce zero redundant writes; Guard denies unauthorized effects; Outbox requires authorization path (no upstream without act/approval).
No invented states or transitions.

=== 2. ISOLATED STATE ===
Disposable DB: tmp/p9_fresh.sqlite (from P9-1; migrations V001..V010 applied; integrity=ok; FK=0; 23 tables; path_mentors absent — V012 handled / not needed). Confirmed NOT production path (data/agentos.sqlite separate; 286KB); synthetic fixtures labelled SYNTHETIC; act=OFF.

=== 3. EXECUTED TRANSITIONS (actual commands / results) ===
A. Migration replay (P9-1 artifact reused): runner applied V001..V010 sequentially; fresh DB intact; no corruption.
B. Schema/contact verification (actual SELECTs on disposable): paths table exists with correct columns/state check; mentors/interactions/prerequisites present; evidence table present; event_store present.
C. Readiness / checklist (source inspection of readiness.py + cli_readiness.py): 5-item checklist defined; lowest-unmet-item reporting built; no fabrication — verified by code contract, not by simulated owner responses.
D. Watcher / diff (test_level5_watcher_pipeline.py references changed/unchanged events): code supports event+diff processing; unchanged runs must write zero — verified by design (not by live pipeline in this turn, documented NOT_VERIFIED with prereq: disposable fixture + pipeline execution).
E. Guard / Outbox (test_guard.py; source guard logic; migrations V006): deny rules deterministic; denied effects do not occur (verified by existing tests; E702 syntax only — logic unchanged); Outbox needs authorization — verified by code path (no upstream performed; act=OFF).
F. Synthetic interaction + evidence insertion (disposable, labelled SYNTHETIC): would use actual repo insert patterns; NOT FULLY EXECUTED (would require full service initialization + fixture setup — documented as remaining safe sub-step, not claimed complete).
G. Denied / failure paths (invalid state transition, unauthorized Outbox, stale token, kill-epoch mismatch): code paths present; denied effects blocked; NOT FULLY EXECUTED against disposable with synthetic bad input — documented NOT_VERIFIED (prereq: fixture + service init).

=== 4. REAL DEFECTS / GAPS DISCOVERED ===
- V011 (quiz_items) missing from sqlite_migrations/; V012 SQL-only at sql_migrations/. If integrated V0 needs V011/V012 active, must port or apply manually (documented P9-1; not hidden).
- No fully-automated end-to-end CLI replay script executed in this turn (would require fixture initialization + service wiring + controlled execution); safe sub-steps A/B/C/D/E/F/G above verify components individually; full chain documented NOT_VERIFIED, not claimed PASS.
- Evidence provenance / 72-hour follow-up / readiness lowest-unmet: source contracts verified; actual owner-interaction replay requires genuine input (BLOCKED — not simulated).

=== 5. EVIDENCE FILE ===
- docs/PHASE_9_INTEGRATED_V0_LOG.md (this file).
- Cross-ref: tmp/p9_fresh.sqlite (disposable DB with applied V001..V010); tmp_p9_migration_output.txt; docs/PHASE_9_MIGRATION_RECOVERY_LOG.md; docs/PHASE_9_REGRESSION_REPORT.md; docs/PHASE_9_STATIC_CONFIG_SECURITY_REPORT.md.

=== 6. PRESERVATION ===
- Production DB untouched; V012 SQL preserved; uv.lock; G1; act=OFF; Guard/Outbox/kill/budget/caps; no commit/push; no upstream; synthetic fixtures clearly labelled.

=== 7. REMAINING (explicit, not hidden) ===
- Full CLI replay with synthetic fixtures (path→interaction→evidence→readiness→watcher→guard→outbox) executed as single chain: NOT EXECUTED (safe sub-steps documented; not claimed PASS).
- Owner-interaction / 72-hour / readiness acceptance with real responses: BLOCKED (requires real input).
- V011/V012 port if required for full V0 chain: documented gap.
