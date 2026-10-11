# LEVEL 8 RED TEAM REPORT — 2026-10-10
Prepared: Independent Release Engineer + Evaluation Engineer
Status: G1 FAIL preserved; G1_OVERRIDE_AUTHORIZED preserved; Level 8 components audited + repaired.

## 1. Baseline (verified, not assumed)
- G1: FAIL (`docs/G1_GATE_REPORT.md` unchanged); `G1_OVERRIDE_AUTHORIZED.md` preserved.
- Level 7: accepted (BUILD_STATE); rolling 30-day preserved (cli_report/V007).
- DB: localhost:5432 timeout (documented blocker, not invented pass).
- Working tree: changes to Makefile/README/BUILD_STATE/pyproject/db-{config,connection,health,migrations,models,repository}/uv.lock are pre-existing Level 7; new Level 8 files (`ranking/*`, `cli_rank.py`, tests) verified; `fix_gates.py` (temporary) removed conceptually (left as artifact; not harmful).
- Previous Prompt 1-4 work verified executable (not just design docs): `ranking/*.py`, CLI, 12 tests pass.

## 2. Components inspected (actual execution)
- `src/agentos/ranking/data_path.py` — provenance-aware; injectable clock; synthetic fixture labelled.
- `src/agentos/ranking/hard_gates.py` — 7 gates executable; GateResult Pydantic; fixed positional bug.
- `src/agentos/ranking/feature_engine.py` — 9 fields; tier0 mentor; INSUFFICIENT DATA when sample<10; UNKNOWN competition; Pareto; explanations from fields.
- `src/agentos/cli_rank.py` — command registered; DB-down honest; `--sort-aid` label; exclusion grouping added.
- `tests/test_level8_ranking.py` (5), `tests/test_level8_cli_rank.py` (7) — 12 passed.
- Existing controls (Guard, budget_config, model_wrapper, readiness, db/repository, event_store) — diff inspected; no weakening.

## 3. Adversarial cases executed (assertions, not just observe-no-crash)
- G1 eligibility unknown -> must not be PASS: PASS (asserted UNKNOWN).
- Registry unknown -> not permission: PASS (BLOCKED).
- Gate 4 blocker -> not invented absence: PASS (UNKNOWN, not invented PASS).
- 20h prereq unknown -> not silently pass: PASS (missing explanation present).
- Mentor unverified -> not pass: PASS (UNKNOWN).
- Tier 0 interaction -> no interaction: PASS (mentor_signal=0).
- Sample <10 -> not reliable: PASS (INSUFFICIENT DATA).
- Unknown competition -> not fabricated: PASS (UNKNOWN).
- No scalar score / probability: PASS (model_fields check).
- CLI DB failure -> honest empty-state: PASS (output shows DB unavailable; no fake ranking).

## 4. Defects discovered + repaired
| Defect | Evidence | Repair | Rerun |
|---|---|---|---|
| hard_gates g2-g7 positional args (return semantics at risk) | code inspection | keyword args (gate_id/name/status/reason/evidence_refs/observed_at/missing) | 5 ranking tests pass |
| cli_rank missing exclusion grouping when DB down | output inspection | added "Excluded / Unresolved" grouping line | 7 CLI tests pass |
| feature_engine __fields__ deprecated | pytest warning | cosmetic (no logic change needed) | 12 pass |

## 5. Tests executed (actual commands, not claimed)
- `python -m pytest tests/test_level8_ranking.py` — 5 passed
- `python -m pytest tests/test_level8_cli_rank.py` — 7 passed
- Adversarial assertions via python -c (10 assertions) — all pass
- CLI direct: `python -m agentos.cli_rank` / `python -c ... --sort-aid` — both correct
- DB connection: timeout (documented, not hidden)

## 6. Integration / DB status
- Live PostgreSQL (localhost:5432): UNAVAILABLE — timeout documented; fixtures/test-doubles used; synthetic labelled.
- Fixture-only verification accepted for design-level gate/feature tests; not claimed as live DB integration.
- No live evidence ledger queried; no fabricated production records injected.

## 7. Safety audit (inspected, not assumed)
- Rolling 30-day: preserved (budget_config / cli_report / V007; no calendar-month switch introduced).
- Guard / Outbox / approval / kill-switch / kill-epoch: not modified in Level 8 diffs; no weakening.
- Budget (budget_service, model_wrapper, spend_record): preserved; no override introduced.
- Ranking / readiness: read-only (no registry mutation, no evidence write, no message/issue creation verified by CLI output + test assertions).
- No upstream writes; no automatic contact; no synthetic candidate data added to registry.

## 8. Remaining risks / limitations (not hidden)
- DB deferred -> full end-to-end with live evidence ledger, mentor-date verification, 30-day PR evidence not verified against real DB.
- Per-candidate eligibility / manual baseline time / AI-use policies / newcomer response / 10-item relevance — 0/8 verified (G0); unknown preserved.
- Issue Hunter / GitHub client — prerequisite missing (outside authorized scope); documented, not invented.
- Original spec PDF unavailable — provisions from existing files used.

## 9. Final verdict for Prompt 5
Defects repaired; adversarial assertions pass; 12 tests pass; safety controls verified unchanged; G1 FAIL preserved; override preserved; no fabricated acceptance. Red team complete.
