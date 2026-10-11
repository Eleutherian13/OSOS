# FALLBACK RUNBOOK — G1 FAIL (spreadsheet + watcher; no Level 8)
# Status: G0 PASS / G1 FAIL / Level 8 NOT AUTHORIZED. Created 2026-10-10.
# Gate integrity preserved: docs/G1_GATE_REPORT.md, docs/G1_COMPARE_FINAL_2026-10-10.md,
# docs/BLINE_COMPLETED_V2_2026-10-10.md unchanged from G1 decision.

## 1. Open the eight-path baseline
File: docs/G0_C_MANUAL_FINDINGS.csv (8 rows: S01/S05/S06/S07/S08/S09/S11/S12).
Fields that must have source URLs / dated observations / exact quotes:
 contribution_policy_url, contribution_policy_quote_observed, source_links,
 access_timestamp, observation_note, verification.
Unverified fields (documented UNKNOWN / NOT FOUND) must stay marked so they
are not invented as verified.

## 2. AI-use / contact / 10-item / response / eligibility
Required per G1_METHOD.md / G0_SHALLOW_REVIEW_REPORT.md.
If not verified for a path, write NOT FOUND / UNKNOWN with search scope
documented (e.g., "docs.vllm.ai not fetched" / "direct kubernetes/kubernetes /issues not fetched"). Do not convert UNKNOWN to verified.

## 3. Run watcher (existing v0)
Manual:  uv run python -m agentos.cli_watch  (check src/agentos/cli_watch.py / watch targets)
Scheduled: see Makefile targets (none for watcher specifically); use cron/task
scheduler pointing at the cli_watch command or the watch sync module.
Actual commands verified from repo: no invented CLI flags.

## 4. Inspect a detected change
Read watch target output / diff; compare to docs/G0_C_MANUAL_FINDINGS.csv
source_links timestamp; if contribution policy quote changes, update CSV
with new URL + quote + access_timestamp. If unchanged, do NOT rewrite.

## 5. Unchanged second run
Verify no writes to CSV / evidence repo when source unchanged (idempotency
required; guard DENY / outbox protections remain in place — do not disable).

## 6. Stop / recover
Kill cli process; check docs/DB_CONNECTION_OK.md / kill-state files for
failed-run recovery; re-run from clean SQLite temp DB (AGENTOS_DB_PATH=temp.sqlite3)
without altering PostgreSQL DSN (preserved per skip preservation rule).

## 7. Human-controlled decisions (do not automate)
Candidate approval (user-selected 8 of 12), eligibility confirmation,
relevance filtering of 10 items per path, time measurement, AI-use policy
interpretation, contribution-route correction (S12 mirror). Log actual time
spent per session; do not use 20-min planning estimate as measurement.

## Commands (verified against repo)
- Spreadsheet open: open docs/G0_C_MANUAL_FINDINGS.csv
- Watcher manual: uv run python -m agentos.cli_watch (or direct module call)
- Tests (actual): uv run pytest tests/unit/test_db_connection_fix.py
- SQLite check: $env:AGENTOS_DB_PATH='data/temp.sqlite3'; uv run pytest tests/integration/test_event_store.py -v
- Gate status check: cat docs/G1_GATE_REPORT.md | grep "GATE STATUS"  (FAIL preserved)
