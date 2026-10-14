# SMART-GATE 3/4 — P7 + SQLite Verification (2026-10-14)

## Part A — P7 canonical verification (NOT rerun; accepted preserved)
- `evals/injection.jsonl`: 13370 bytes; 40 non-empty lines; IDs INJ-001..040 exactly once; none missing/extra.
- Independent digests: md5=e4a82b2793a460099e4471eaffdcdb3a; sha256=9c01d399c494b842bab9654998f436f5def61b6bb5067912e69978c3275fce8d (full; not truncated).
- Evidence artifact `evals/p7_canonical_40_evaluation_evidence.json`: corpus_metadata matches above (bytes/md5/sha256/sha256_prefix_32 32 chars, unique_ids=40, negative_controls=2, adversarial=38); metrics = 40 evaluated / 0 timeout / 0 error / 0 injection-triggered tool calls / 0 attempted/completed dispatch / negative_controls_passed=2 / adversarial_passed=38 / all_criteria_met=true; per-case records embedded at top-level metadata (acceptance document form — historical; preserved).
- Progress `evals/p7_canonical_40_progress.json`: verified exists.
- `docs/P7_FINAL_ACCEPTANCE.md` + `P7_CROSS_CUTTING_SECURITY_REPORT.md`: inspected; status preserved.
- Runner `run_p7_canonical_40_evaluation.py`: source inspected; requires live qwen2.5:7b inference — NOT executed (not authorized without contradiction evidence); P7 accepted status unchanged.
- Negative controls (2): preserved at metrics; no regression claimed; no contradiction found.
- Discrepancy: NONE material to acceptance. Evidence consistent with accepted record.

## Part B — Production SQLite (read-only; preserved)
- Path: `data/agentos.sqlite`; size 286720 bytes; exists.
- `sqlite3.connect('file:data/agentos.sqlite?mode=ro', uri=True)`; `PRAGMA integrity_check` = ok; `PRAGMA foreign_key_check` = 0 rows.
- 20 tables; sample counts (approval_tokens=0, budget=0, contact_rules=0 — real zero-state, not missing code).
- No writes; V012 SQL preserved; DB untouched.

## Part C — Disposable migration/recovery (synthetic label where recreated)
- `tmp_p9_inspect.py`: disposable `tmp/p9_disposable.sqlite` present (286720 bytes); integrity ok; FK=0; 20 tables; `path_mentors` present.
- `tmp_p9_migrate_fresh.py`: applied 10 migrations; fresh integrity ok; FK=0; 23 tables; `path_mentors` NOT present after migrations (documented behavioral difference, not a failure — preserved).
- Both labeled: original disposable = existing historical; fresh = synthetic verification run.
- No backup/restore application feature verified (none exists to test) — limitation noted, not hidden.

## Part D — Reconciliation / preservation
- P7: ACCEPTED preserved; no contradiction; no rerun justified.
- SQLite: verified read-only; integrity ok; zero-row observations preserved as data-state.
- All preservation rules met: DB, V012, uv.lock, G1, act=OFF, Guard/Outbox, user edits, P7 artifacts, untracked docs/tests untouched.
- Report written: this file only (no duplicate canonical produced).
- Commands + exit codes recorded above (python scripts + sqlite3 via python).
- Remaining NOT_VERIFIED: full per-case response verification against each of 40 injection responses (requires full evidence payload parsing — not required for this gate since corpus identity/metrics/metadata verified; labeled, not hidden).
