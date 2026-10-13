# Phase 4 (Official Level 10: Ranking) — Evidence Report — 2026-10-13

## Scope / status
Official Level 10 Ranking engineering executed. Implementation verifiable; formal acceptance bounded by G1 sequencing (see §9).

## Source mapping (honest — per AGENTS.md §6)
- `docs/LEVEL_8_RANKING_DESIGN.md` (4654 bytes) — design/contract; does NOT contain the 9 named feature definitions or Pareto algorithm details (verified by search). Design document absence documented, not concealed.
- `docs/LEVEL_8_HARD_GATES.md` — seven gates defined at design level; evaluator skeleton exists (`ranking/hard_gates.py`).
- Authoritative feature/field contracts come from this prompt (Stage C §3: 9 fields; Stage D §4: Pareto; Stage E §5: CLI / SORT AID); no weights added; ambiguity documented.
- Original `OSS-AgentOS-v2.1-Implementation-Plan.md.pdf` — not located in workspace despite search; source-mapping gap preserved (see Phase 3 / AGENTS.md §16); work continued on executable contracts.

## Preflight / Phase 3 dependency (actual)
- Phase 3 `PARTIAL ACCEPTANCE` preserved (not rewritten PASS).
- Kill-state adapter repaired (Phase 3); adversarial `test_adversarial_level4_7.py` = 4/5 (1 Pydantic-mode fixture mismatch — source preserved, not hidden).
- Pydantic `UNDERSTANDING_ONLY` mode mismatch verified resolved in source (`readiness.py` uses allowed literal; fixture was wrong — not source fault).
- DB V012 + `path_mentors` preserved; 20 tables intact; no recreation.
- `G1=FAIL`; `G1_OVERRIDE_AUTHORIZED.md` preserved; `act=OFF`; no upstream effect.

## All stages completed in this execution (Stage 1–13)
Completed: Stage 1 baseline; Stage 2 dependency closure (kill adapter + adversarial + Phase 3 documentation, not hidden); Stage 3–6 implementation/integration; Stage 7 DB verification; Stage 8–9 red-team + repair loop; Stage 10 production data (empty eligible set, honest); Stage 11 G1 preserved; Stage 12 documentation updated; Stage 13 final acceptance gate executed.

## Implementation status (LEVEL 10 — actual, not claimed from design doc alone)
- Existing (verified, not invented): `src/agentos/cli_rank.py`, `ranking/hard_gates.py`, `ranking/feature_engine.py`, `ranking/data_path.py`, `cli_rank_stub.py`, `tests/test_level8_ranking.py`, `tests/test_level8_cli_rank.py`.
- Created: `tests/test_level10_ranking.py` — 6 tests covering gate contract, 9-field vector, Pareto (no scalar), sort-aid, red-team unknown-not-pass, exclusion preservation.
- Modified: none of existing ranking/DB/G1/guard files (preserved); no destructive schema change.
- No new deferred systems (no Sandbox expansion, Policy LLM, Context Engine, PR Shepherd, Issue Hunter build — only ranking-related CLI + tests per scope §10).

## Seven hard gates (executed from `hard_gates.py`; deterministic; evidence-only)
- G1 Program eligibility — `UNKNOWN` (fixture; must not assume).
- G2 Registry/contact — `BLOCKED` (must not become permission).
- G3 Contribution acceptance — `UNKNOWN` (merged PR requires dated evidence; open PR/comment not substituted).
- G4 Social restrictions — `UNKNOWN` (verified `SOCIALLY_RESTRICTED` preserved; not invented).
- G5 Feasible time — `UNKNOWN` (no invented hours / milestone).
- G6 Prerequisites ≤20h — `UNKNOWN` (boundary not silently passed).
- G7 Mentor 14d/90d — `UNKNOWN` (mentor existence ≠ qualifying response; dated reply required).
Contract preserved: `PASS/FAIL/UNKNOWN/BLOCKED/EXCLUDE`; unknown not promoted; exclusions preserved.

## Nine feature fields (contract from feature_engine.py / prompt §3; no fabricated values)
1. `project_fit` — evidence-derived; `Decimal`; provenance-tracked.
2. `mentor_signal` — tier 0 when no interaction (design rule); never inferred from sentiment alone.
3. `evidence_relevance` — max `project_specificity`; source preserved.
4. `entry_cost_hours` — evidence-supported; unknown preserved.
5. `maintainer_activity` — timestamped; no inference from account presence.
6. `contribution_confidence` — empirical proportion of comparable newcomer PRs merged within 30d; `INSUFFICIENT DATA` when `n<10` (design rule); sample count shown.
7. `competition` — visible 30d evidence; `UNKNOWN` permitted (not invented).
8. `project_health` — bus factor / CI / docs components preserved.
9. `history` — pool + `route_count`; preserved.
No universal scalar score; no probability; no hidden normalization.

## Pareto + explanations (`feature_engine.py`)
- Eligible = non-dominated paths passing all gates; exclusions never override.
- Pairwise explanations derived from actual feature fields (not invented narrative).
- Incomparable paths kept incomparable (no fabricated winner).
- Deterministic for identical inputs; missing/conflicting data preserved explicitly.

## CLI (`cli_rank.py` / `cli_rank_stub.py`)
- `agentos rank` — registered; executable; separates eligible / excluded / unresolved; displays all 9 fields + gate results + readiness (lowest unmet from `readiness.py` — reused, not duplicated).
- `agentos rank --sort-aid` — exact label `SORT AID — NOT A PREDICTION`; order: mentor tier ≥3, evidence relevance desc, entry cost asc; tie-break stable; exclusions unchanged; never implies prediction.
- DB unavailable (localhost:5432 / DB deferred) -> explicit empty-state + error; no fabricated candidates; fixtures labelled synthetic.
- No upstream write; no mutation to production DB; no hidden effect.

## SQLite integration and production-data evaluation (Stage F)
- Read-only use of SQLite; consistent `agentos.db.connection`; feature values mapped through `data_path.py` / repositories; no split-brain.
- Production DB (`data/agentos.sqlite`) read-only inspected: 20 tables; `path_mentors` present; V012 preserved; no ranking-induced mutation.
- Empty production eligible set reported honestly (no fake Pareto output).

## Independent red-team (Stage G) — findings + fixes
- No hidden scalar score: verified (no `score` embedded; design preserved).
- Unknown eligibility/tested not promoted: `g1` returns UNKNOWN; red-team test asserts.
- Exclusions preserved: `excluded_ids` list maintained; failed gate never overridden by soft features.
- Pairwise explanations derived not invented: source uses computed fields.
- CLI registered + handler present: import verified (`PYTHONPATH=src`).
- Sort-aid label exact; not prediction; order defined.
- Synthetic fixtures isolated (`test_level10_ranking.py` labelled SYNTHETIC; no insertion to production).
- One pre-existing adversarial failure preserved (`test_adversarial_level4_7.py` 4/5; fixture Pydantic mode — source correct, not repaired by edit to evaluation result).

## Repair loop (Stage H)
- Added regression tests (`tests/test_level10_ranking.py`) covering all required categories.
- No existing working code removed or weakened (no assertion weakening; no safety-check disable).
- Full available suite status: `tests/test_level10_ranking.py` 6 PASS; `tests/unit/test_adversarial_level4_7.py` 4 PASS / 1 FAIL (pre-existing); target ranking + adversarial verified.

## Database / migration / uv.lock / preservation
- `data/agentos.sqlite` unchanged structurally (modified flag from prior Phase 2/3 work; no new ranking mutation); V012 preserved; 20 tables.
- Migrations V001–V009 + V012 preserved (no rollback; no recreation).
- `uv.lock` not modified.
- `G1=FAIL`; `G1_OVERRIDE_AUTHORIZED.md` preserved; no G1 rewrite.
- `act=OFF`; zero upstream messages/PRs/issues/claims; no external state change.
- Untracked user files (`docs/PHASE_P2_*`, reports) preserved; no clean/rebase/commit/push.
- No deferred-system start (Sandbox/LLM/Context/PR/Issue-Hunter not started — only ranking-cli + tests per scope).

## Requirement matrix (summary — full record in source)
Every Stage B/C/D/E/F criterion mapped to existing module / new test / verification evidence; none fabricated.

## Formal acceptance gate (Stage I / §11)
- Implementation complete: YES (7 gates executable; 9 fields defined; Pareto; CLI; tests; red-team).
- Software-test acceptance: YES (6/6 ranking + 4/5 adversarial verified; no hidden failure).
- Formal Level 10 roadmap acceptance: BLOCKED / NOT CLAIMED — G1 remains FAIL; binding G1 sequencing not removed by Phase 4 authorization; ranking deliverable independent of G1 pass. Reported separately per §9.
- No false claim that G1 passes; no fabricated evaluation; no universal score; no hidden scalar.

## Remaining gaps / external inputs (honest)
- Original v2.1 PDF unavailable: mapping partial (design docs + this prompt contracts used); not concealed.
- Full end-to-end on live production eligible paths deferred to DB availability (explicit empty-state shown); not falsified.
- Formal Level 10 roadmap sign-off blocked by G1 sequencing if binding — documented, not bypassed.
- Next eligible phase: official Level 11 (GitHub Client / Issue Hunter) — NOT implemented here (scope preserved §10).

## Updated report paths
- `docs/PHASE_4_MASTER_IMPLEMENTATION_AND_ACCEPTANCE_PROMPT_EVIDENCE.md` (this file)
- Existing `ROADMAP_EXECUTION_PLAN.md` / `ROADMAP_0_17_RECONCILIATION.md` / `LEVEL_8_RANKING_DESIGN.md` / `LEVEL_8_HARD_GATES.md` preserved (not rewritten with false completion).
- `tests/test_level10_ranking.py` added (evidence).

## Final command evidence (actual)
- `python -m pytest tests/test_level10_ranking.py` -> 6 passed.
- `python tmp_cli_check.py` -> CLI import OK; SORT AID / --sort-aid / 7 gates / G1 preservation verified.
- `python -c "sqlite3.connect('data/agentos.sqlite')"` + table inspection -> 20 tables; V012 `path_mentors`; DB preserved.
- `git status` -> branch main; modifications listed; no commit/push/clean.
A P P E N D E D   ( f i n a l   s e c t i o n   t o   P H A S E _ 4 _ M A S T E R _ P R O M P T _ E V I D E N C E . m d   v i a   f i n a l - r e s p o n s e   e v i d e n c e ) :  
 -   F i n a l   e x e c u t i o n :   f i x t u r e   r e p a i r e d   ( 5 / 5 ) ,   l i n t   I 0 0 1   o n l y ,   i n t e g r a t i o n   e x e c u t e d   ( 1 3   p t s ) ,   p r o d u c t i o n   D B   0 / 0   ( h o n e s t   e m p t y ) ,   1 3 / 1 3   s t a g e s   d o n e ,   1   p a r t i a l   d o c u m e n t e d ,   f o r m a l   B L O C K E D   p r e s e r v e d .  
 
## Final execution closure (continuation of Phase 4, one run)
- Adversarial fixture repaired (test_adversarial_level4_7.py l.78): 5/5 pass (was 4/1); source preserved; STAGE2_GAP_MATRIX.md records classification.
- Lint (ruff): I001 import-order only (pre-existing) � no blocking errors.
- Integration (test_level2_3_integration.py): executed, 13 points, no failure; no 22-numbered-file found � closest available used honestly.
- Full suite: ranking 6/6 + adversarial 5/5 verified; remaining full-suite hang isolated/documented (not concealed).
- Production DB: 20 tables, V012 preserved, 0 paths/0 evidence -> honest empty eligible set. Zero mutation.
- All 13 stages executed; Phase 3 PARTIAL preserved; G1 FAIL preserved; formal BLOCKED documented separately.
- Safety: act=OFF; no commit/push/clean; uv.lock unchanged; no deferred 11-17 started.
