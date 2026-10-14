# PHASE 9 — PRODUCTION HARDENING & FINAL ACCEPTANCE (P9) — LEVEL 17 — 2026-10-14

CONTROLLING: AGENTS.md §14/§15/§16; v2.1 plan §4 (CORE/NEXT/DEFERRED) + §14 (test discipline); docs/PHASE_8_FINAL_ACCEPTANCE.md (P8 verified PASS / real-E2E BLOCKED / Design B DEFERRED / G1=FAIL preserved); docs/PHASE_9_ENTRY_CHECKLIST.md; docs/G1_OVERRIDE_AUTHORIZED.md (authorize continued dev, NOT pass); docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md (L11 only); docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md.

AUTHORITATIVE CORRECTIONS APPLIED BEFORE ANY STATUS CLAIM (the user's 6 points):
1. L2-3 empty DB ≠ missing impl. Verified CLI/repos/validations/tests vs v2.1 acceptance (test_level2_3_integration.py); real-data acceptance kept separate.
2. L8 vs L9 / G1: G1=FAIL preserved in both copies (docs/ present; root copy NOT PRESENT — contradiction documented, not hidden). G1_OVERRIDE_AUTHORIZED permits continued development; does NOT convert FAIL→PASS, does NOT auto-block L8/L10/L11/L12/L16 work.
3. L11: 50-issue benchmark BLOCKED (missing grounded labels). 13/13 reported tests preserved as implementation verification only (not benchmark). Sandbox Stage B evidence NOT used as Issue Hunter correctness proof.
4. L12: syntax/test-collection checked (tests/test_auditor_domain.py exists; syntax repaired via fix_syntax.py earlier). Golden-answer eval requires genuine owner input (tests/level10_owner_labelling_session{1,2}.md present but not self-certified); no simulated owner/time.
5. L14 (Sandbox): existing work (sandbox/, LEVEL_11_SANDBOX_*.md, test_level11_sandbox_orchestrator.py) preserved. NOT expanded to full L14 official acceptance — trigger + amendment scope unresolved; act=OFF kept.
6. L16 (Design A / Proposal Auditor): Design A accepted for scoped use (PHASE_8_FINAL_ACCEPTANCE.md §3 PASS; service/edit + 17 synthetic tests). Real E2E BLOCKED (DB evidence=0; proposal/idea/hours missing). Design B deferred (separate auth/dataset/method); neither blocks unrelated CORE.

SCOPE DISCIPLINE MAINTAINED (v2.1 §4): CORE completed during P2/P3; NEXT (L8 ranking, L9 client, L10 quiz/reviewer, L11 benchmark-prep, L16 auditor) preserved; CONDITIONAL deferred (L13 Context Engine — not bottleneck; L14 Sandbox — trigger unresolved; L15 PR Shepherd — no real PR workflow yet; Policy LLM — scale <12; Design B — deferred). No deferred subsystem promoted without trigger.

=== P9 PHASE OBJECTIVE ===
Not a feature phase — a verification/hardening/reporting phase. Final matrix must distinguish: IMPLEMENTED / VERIFIED / NOT VERIFIED / BLOCKED / DEFERRED, with evidence per cell. Every claim mapped to code/test/docs/artifact (file:line or file reference), never restated from prior report alone.

=== P9 SUB-PHASES (must all complete with evidence; nothing omitted) ===

P9-1  MIGRATION / RECOVERY / SCHEMA HARDENING
- Verify every migration executes cleanly (V001..V011 in migrations/; V012 sql_migrations/V012__path_mentor_remove.sql — note V012 is SQL-only, check if applied to SQLite path). Run against disposable SQLite DB (.env points to file; verify path in config/ or .env.example).
- Migration/recovery tests: create disposable DB, apply V001..V012 in order, confirm schema matches expected (migrations/V002 mentor_project_path; V003 evidence; V006 kill/outbox; V010 issue_hunter; V011 quiz; V012 removal). Restore from backup path (test using sql_migrations/ restore script if present).
- Acceptance: migrations idempotent, no destructive desc (AGENTS.md §5); SQLite-compatible (no PG-only features); V012 removal does not corrupt mentor_path data unexpectedly.
- Evidence file: tests/integration/test_migration_recovery.py (new, SYNTHETIC fixtures; labelled).
- Blocked if: production DB not SQLite (see DB_CONNECTION_OK.md / DB diagnostics in docs/); if SQLite path unknown, document rather than invent.

P9-2  REGRESSION / FULL RELEVANT SUITE
- Run full relevant suite per AGENTS.md §14: pytest on tests/ (targeted by component: test_level2_3, test_level7_budget, test_level8_ranking/cli, test_level9_client/issue, test_level10_quiz/reviewer/ranking, test_level11_sandbox, test_level12_adversarial, test_auditor_domain + new validation/contract, cli/). Include new P9 integration.
- Must verify: syntax error absence (re-check with ruff check .; mypy .); test collection passes (no collection errors from syntax); no hidden failures masked by skips.
- Preserve reported counts honestly: P7 40-evaluation results (run_p7_canonical_40_evaluation.py / tmp_p7_final_*.json) preserved as historical; not rewritten as PASS; P6 L12 tests preserved (test_level12_adversarial_grading.py etc.).
- Acceptance: exit 0 on relevant target; failure counts reported exactly (not rounded to 0); any skip annotated with reason (external dependency / missing service / blocked by missing dataset — not hidden).
- Commands recorded (actual): uv run pytest tests/test_level2_3_integration.py tests/test_level7_budget_engine.py ... (targeted runs per component); uv run ruff check src tests; uv run mypy src tests; results captured to docs/PHASE_9_REGRESSION_LOG.md.

P9-3  STATIC ANALYSIS / CONFIG / LOGGING / SAFETY CONTROLS (P2 preservation verified)
- ruff lint + format check: src/, tests/, cli/ — no regressions from P2 fixes (registry, Guard, Outbox, kill, budget, hours, watcher).
- mypy strict: src/agentos/ (agentos package); confirm typed contracts (Pydantic v2) for registry, evidence, mentor_path, ranking, quiz, reviewer, auditor_service.
- Config validation: config/budgets.yaml, config/prices.yaml, config/programs.yaml valid; .env.example / .env real values only in non-committed scope (AGENTS.md §7 secrets).
- Safety controls audit (P2 / P7 accepted at design/test): Guard denial rules all have tests (verify per test level); Outbox rejects stale/unauth; authorization tokens checked; kill-epoch enforced; budget rolling-30-day enforced (not calendar-month); act=OFF (docs/LEVEL_11_SANDBOX_*.md; no upstream automated); no secret in src/ / tests/ / new docs.
- Evidence: ruff/mypy output files; config-check script output; guard-test reference list.

P9-4  INTEGRATED V0 WORKFLOW (L8 + CORE) — PRESERVED, NOT REWRITTEN
- Re-run P3-style integrated CLI/SQLite path (path creation → interactions → evidence → readiness → watcher events → Guard/Outbox) in isolated disposable DB — ONLY verification, not new feature.
- Acceptance (P3 criteria preserved): components interoperate; invalid transitions rejected; unauthorized effects blocked; safeguards hold; G1 historical FAIL preserved independent of flow.
- Blocked if: CLI entry points missing (cli/); DB path unconfigured — document, don't fabricate.

P9-5  COMPONENT VERIFICATION BY PHASE (each must have evidence — pass, fail, blocked, or deferred; no silent omission)
- L2-3 Mentor/Evidence (P1): CLI + repos + validations + tests verified; empty DB handled honestly (tests/test_level2_3_integration.py; db_counts.py reference); real-data acceptance SEPARATE (not claimed from synthetic fixtures).
- L4-7 CORE (P2): registry, watcher, Guard, Outbox, auth, kill, budget, hours — audit only demonstrable gaps; changed pages → events; unchanged → no redundant writes; invalid registry fails closed; every Guard denial tested; stale/unauth outbound rejected; rolling-30-day; act=OFF.
- L8 Ranking (P3): seven hard gates, nine dimensions, Pareto, sort-aid (not universal score), provenance — verified against real interfaces (test_level8_ranking.py / test_level8_cli_rank.py); missing evidence = unknown; hard-gate failures visible.
- L9 Client/Issue Hunter (P5): ETags, rate limit, backoff, transitions, restriction handling, provenance — verified vs docs/LEVEL_9_*.md; benchmark BLOCKED (no fabricated label); claim is “no public evidence someone else is on this” (never “free”).
- L10 Quiz/Reviewer (P6): syntax/collection fixed; rubric ≥80% rubric facts; 30 golden answers with source lines (LEVEL_10_GOLDEN_ANSWERS.md); ≥10 experimentally verified; owner labelling session artifacts preserved (level10_owner_labelling_session*.md) — NOT simulated as passed; evaluator metrics only when valid labels exist (BLOCKED until owner provides second session + 7-day gap verified).
- L11 Issue Hunter (P5): 13/13 tests preserved; Stage B evidence NOT benchmark; benchmark evaluation BLOCKED until 50 genuinely sourced + human-labelled (docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md applies to entry only).
- L12 Quiz/Grader (P6): syntax repaired (fix_syntax.py; current collection verified); adversarial grading verified (test_level12_adversarial_grading.py); golden answers exist; owner-input BLOCKED for final eval.
- L16 Proposal Auditor (P8 / P9-8): Design A implemented (auditor_service.py edit + 2 test files + doc); 17 synthetic PASS; real E2E BLOCKED (DB evidence=0; input prerequisites listed in PHASE_8_FINAL_ACCEPTANCE.md §5); Design B deferred (separate authorization/dataset/method); no rewrite of P8.
- P7 Security (cross-cutting): injection corpus preserved (red_attack.py / red_batch.py / run_p7_canonical_40_evaluation.py); zero-triggered-tool-call / zero-out-of-enum-field criteria maintained; adapter isolation (test_llm_adapter_isolated.py); secret hygiene verified (no secrets in new artifacts); outward authorization (Guard/Outbox/approval) enforced.

P9-6  FINAL ACCEPTANCE MATRIX (must be this file or a referenced doc; not reconstructed from memory)
Template per line: COMPONENT | IMPLEMENTED | VERIFIED | BLOCKED / REASON | DEFERRED / REASON | EVIDENCE
Filled honestly (no hidden FAIL→PASS):
- L2-3 Mentor path: IMPL | VER (tests, CLI) | — | — | test_level2_3_integration.py; cli/
- L3 Evidence engine: IMPL | VER | — | — | V003/V012; tests/
- L4-7 CORE: IMPL | VER | — | — | P2 reports; guard/registry tests; budget/hour tests
- L8 Ranking: IMPL | VER | — | — | test_level8_*.py; LEVEL_8_*.md
- L9 Client: IMPL | PART (ETags/backoff/provenance verified; live endpoint limitations preserved) | benchmark BLOCKED | — | LEVEL_11_* docs; test_level9_*.py
- L10 Quiz/Reviewer: IMPL | PART (tests pass; golden answers present; owner labelling session artifacts exist) | EVAL BLOCKED (2nd session + 7-day gap + owner confirmation required) | — | LEVEL_10_GOLDEN_ANSWERS.md; test_level10_*.py; owner_labelling_session*.md
- L11 Issue Hunter: IMPL | PART (13 tests; Stage B preserved) | BENCHMARK BLOCKED (50 labels missing) | — | LEVEL_11_* reports; AMENDMENT doc; test_level11_*.py
- L12 Grader: IMPL | PART (syntax fixed; adversarial verified) | EVAL BLOCKED (genuine owner labels + 7-day separation) | — | level12_*.py; fix_syntax.py
- L13 Context Engine: — | — | — | DEFERRED (not bottleneck; ripgrep baseline holds) | AGENTS.md §12
- L14 Sandbox: IMPL (existing) | PART (Stage A/B artifacts; security audit) | FULL ACCEPTANCE BLOCKED (trigger + amendment scope unresolved) | — | LEVEL_11_SANDBOX_*.md; sandbox/; keep act=OFF
- L15 PR Shepherd: — | — | — | DEFERRED (no real PR/review workflow yet) | AGENTS.md §13
- L16 Proposal Auditor (Design A): IMPL | VER (service + 17 synthetic) | REAL-E2E BLOCKED (DB=0; inputs missing) | Design B DEFERRED | PHASE_8_FINAL_ACCEPTANCE.md; test_auditor_*.py
- P7 Security: IMPL | VER (corpus + adapter isolation + secret audit) | — | — | P7_FINAL_ACCEPTANCE.md; red_*.py; run_p7_*.py; verify_adapter.py
- G1 Evaluation: FAIL | HISTORICAL (not rewritten) | — | — | docs/G1_OVERRIDE_AUTHORIZED.md; docs/G1_*.md; root-copy absence documented

=== P9-7  CANONICAL EXECUTION-PLAN CORRECTION (reflect the 6 points in the master plan) ===
File updated/created: docs/PHASE_9_EXECUTION_PLAN_CORRECTED.md (or appended to this) — records that the v2.1 status matrix corrections are incorporated into P9 and do not restart P1; L2-3 real-data separated; L8/L9 G1 preserved; L11 benchmark blocked; L12 syntax verified; L14 preserved-not-expanded; L16 Design A accepted / Design B deferred / E2E blocked.

=== P9-8  PROPOSAL AUDITOR REAL-DATA (L16 / P8 continuity — NOT new design) ===
Only when prerequisites (from PHASE_8_FINAL_ACCEPTANCE.md §5) genuinely become available: proposal draft (file/content), idea-page URL + verified retrieval, programme-hours log/entry-cost, evidence-ledger links, owner labels (session2 + ≥7-day gap), source-map confirmation. Until then: no synthetic pass claimed as E2E; DB evidence count preserved; no fabricated mentor/reviewer/label/time.

=== P9-9  PRODUCTION HARDENING ARTIFACTS (deliverables of this phase; nothing omitted) ===
- docs/PHASE_9_FINAL_ACCEPTANCE.md (this file, completed with evidence per section)
- docs/PHASE_9_REGRESSION_LOG.md (actual pytest/ruff/mypy outputs; commands; counts)
- docs/PHASE_9_MIGRATION_RECOVERY_LOG.md (migration apply + restore results; DB path verified)
- docs/PHASE_9_CANONICAL_STATUS_MATRIX.md (corrected; all 6 points embedded; no hidden FAIL→PASS)
- docs/PHASE_9_EXECUTION_PLAN_CORRECTION.md (links 6 corrections to v2.1 plan; does not restart P1)
- tests/integration/test_migration_recovery.py (new, SYNTHETIC fixtures; labelled)
- (optional) run/record of integrated CLI/SQLite verification saved to docs/PHASE_9_INTEGRATED_V0_LOG.md

=== SAFETY / BOUNDARIES (reaffirmed; non-negotiable) ===
- No upstream action; act=OFF (AGENTS.md §7; LEVEL_11_SANDBOX_*); no GitHub posting; no PR merge/close; Outbox only for draft; no auto-approval of outbound.
- No secret in new files; check with grep for .env-like strings; preserve .env.example.
- SQLite only (AGENTS.md §5 / owner switch; do not assume PG port 5432); DB path from config / .env; backup/recovery tested; no fresh-empty-DB to mask missing path.
- No fabricated labels, mentor replies, reviewer findings, benchmark results, golden answers, time passage. Owner labelling session2 requires genuine user input; P9 does not simulate it.
- G1 historical FAIL preserved; no edit to G1_OVERRIDE_AUTHORIZED.md; no claim “G1 now PASS”.
- Design B deferred; no expansion of Sandbox to full L14; no Context Engine start; no PR Shepherd start; no Policy LLM unless scale >12.
- Synthetic fixtures labelled SYNTHETIC; real-data acceptance separated; empty DB handled as missing-evidence not FALSE.
- All edits tracked in Git (no commits/pushes required unless user asks; working-tree status preserved; new docs/test files untracked/added per instruction — user did not request commit, so leave uncommitted with record).

=== STATUS AT START OF P9 (evidence, not assumption) ===
- Branch main; commit 4ac488f (phase 7 completed and freezed); uncommitted: src/agentos/core/auditor_service.py modified; untracked docs/PHASE_8_*.md + tests/test_auditor_*.py + docs/PHASE_9_ENTRY_CHECKLIST.md.
- P8 (L16 Design A) verified PASS; P7 accepted (security); P2-P6 outputs present (reports, tests, docs).
- G1: docs/G1_OVERRIDE_AUTHORIZED.md present (authorize); docs/G1_* reports present; root G1 copy NOT PRESENT (documented contradiction, not hidden).
- DB: SQLite (not PG); path from config/ .env; counts preserved (evidence=0 per P8); no invented production data.
- L11 benchmark: BLOCKED; L12 evaluation: BLOCKED pending owner; L14: preserved-not-expanded.

=== END-OF-P9 DELIVERABLE STRUCTURE (each item must exist with content, not placeholder) ===
1. Executed commands (viewable): uv run pytest [targets] → log; uv run ruff check . → log; uv run mypy . → log; sqlite3 <db> .mode table / SELECT ... → migration/DB logs.
2. Evidence of each sub-phase (P9-1..P9-9) referenced by file path.
3. Final matrix (P9-6) filled; blocked/deferred items named with reason (not omitted).
4. 6 corrections reflected in corrected execution-plan doc; status not falsely upgraded.
5. No new upstream action; no secret; no fabricated evaluation; preserve G1; keep Design B deferred; keep Sandbox partial; keep real-E2E blocked.

If any sub-phase cannot complete due to missing service (DB path unverified, external endpoint unavailable, owner labelling missing), document as BLOCKED with exact missing prerequisite — never substitute with synthetic pass or assume availability.
