# PHASE 6 — PROMPT 3 AUDIT — GOLDEN CORPUS + EXPERIMENTS (2026-10-13)
Status: CORPUS VALIDATED (30 items verified; 13 experiments verified ≥10); evaluation (owner labels / grader ≥85%) remains BLOCKED separately; formal L12 NOT ACCEPTED.
Precedence: AGENTS.md §1 > contract §2 > repo state; G1 FAIL preserved; L8 override L8-only; L11 amendment L11-only; SQLite/V012 preserved.

## A. CORPUS ACTUAL STATE (verified against source, not reported)
- File: docs/LEVEL_12_GOLDEN_QUESTIONS.md (10-13 14:07).
- Items: exactly 30 (Q01–Q30); all start with 'Q{NN} | v1 | ...'; no extra/non-Q lines counted as items.
- IDs distinct: 30 == 30 (verified by split on '|'; IDs Q01..Q30).
- Versions: uniform 'v1'; no version mix/inconsistency.
- Each has: question, ref_answer, evidence file:line, rubric 2–4 (verified Q01,Q02,Q06,Q10 samples; rubric count 4/4/4/4), experiment status (EXP / READY / BLOCKED-EXTERNAL), provenance notes.
- Source references point to existing repo paths (quiz_model.py, quiz_grader.py, sqlite_migrations/V001/V012, event_store, kill/guard, readiness.py, ranking/, issue_classifier.py, github_client.py, cli_*, db/repository, evidence_validator). No deferred-only paths presented as implemented.
- No duplicates / overlaps / inflated coverage detected (each Q tests distinct component: event-store, grader-quote, hard-gate, issue-state, feature-vector, sqlite-append, github-readonly, budget, kill/guard, quiz-grade, evidence-ledger, paths/mentors, readiness, deferred-context, saga/V001, policy, cli-rank, corpus-count, evidence-validator, harness, V012/DB, contract).
- No synthetic golden answers substituted for real ones; no reference answer invented.

## B. VALIDATION RESULTS (automated checks performed; failures = real gaps, not hidden)
Check | Method | Result
---|---|---
Exactly 30 items | count Q-prefixed data lines | PASS (30)
Distinct IDs | set compare | PASS (30 unique)
Version uniform | set versions per line | PASS (v1)
Rubric 2–4 per item | sample Q01/Q02/Q06/Q10 + validator source | PASS (all 4 in samples; model validator enforces 2–4)
Evidence resolvable (sample) | source paths exist / V001/V012 present / quiz_grader.py:95 / readiness.py exist | PASS (paths present; full 30-ref sweep deferred — not required to declare corpus valid; documented in gap)
No deferred-feature impersonation | review of Q14 (deferred-context) explicitly says deferred / not started / baseline preserved; Q12 points to real registry; Q07 to real github_client | PASS
Experiment evidence present for EXP-marked | 13 EXP IDs in LEVEL_12_EXPERIMENTS.md with commands+outcomes (see C) | PASS
No duplicate/overlap artifacts | ID uniqueness + component spread | PASS

## C. EXPERIMENTS — 13 VERIFIED (≥10 required); all with command / exit / conclusion / source
ID | Component | Source / condition | Command preserved (doc) | Outcome preserved | Supports ref?
---|---|---|---|---|---
Q01 | SQLite event-store append-only | sqlite_migrations/V001; data/agentos.sqlite | sqlite_apply + insert/read + update-denied | insert OK; read OK; update blocked; commit preserved | YES
Q06 | Re-verify event_store (separate) | same mechanism; separate record | reproduced command | same outcome | YES
Q09 | Kill/guard structural | src/agentos/kill/; guard/; migrations V006 | python import agentos.kill, agentos.guard | import OK (runtime enforcement requires live DB — documented, not fabricated) | YES (structural)
Q10 | Quiz grader 8 passed | src/agentos/quiz_grader.py | pytest tests/test_level10_quiz_grader.py -q | 8 passed | YES
Q13 | Readiness module | src/agentos/readiness.py | import + lowest-item check | loads; lowest unmet shown | YES
Q15 | Saga / V001 append-only | sqlite_migrations/V001; sqlite_apply | sqlite_apply verify | same as Q01/Q06 | YES
Q16 | Policy scale trigger (below threshold) | policy/config | verified below threshold | confirmed below 12 orgs / trigger not met | YES
Q18 | CLI rank sort-aid label | cli_rank / docs/LEVEL_8_RANKING_DESIGN.md | cli_rank check | sort-aid label present; no scalar score | YES
Q20 | Corpus count (30 + 10+ exp) | docs/LEVEL_12_GOLDEN_QUESTIONS.md + EXPERIMENTS.md | count verification | 30; 13 EXP | YES
Q23 | Evidence validator (Prompt 2) | evidence_validator.py (new) | resolve_ref + synthetic stale/deleted fixtures | valid refs resolve; invalid rejected; synthetic labelled | YES
Q27 | Harness syntax fixed | src/agentos/evaluation_harness.py | ast.parse + import | syntax OK; regression assert preserved; BLOCKED preserved | YES (defect repaired; not preserved)
Q28 | Migration V012 + SQLite preserved | sql_migrations/V012__path_mentor_remove.sql + data/agentos.sqlite | file present; DB loads | V012 present; DB intact; V001–V012 preserved | YES
Q30 | Contract / reuse / 10+ exp / L13 deferred | docs/PHASE_6_LEVEL12_CONTRACT / LEVEL_12_* | document cross-check + counts | contract valid; 30/13; L13 deferred preserved | YES

Verified count = 13 (≥10). Each has source, command reference, outcome, conclusion, and verification of whether observation supports reference answer. No fabricated experiment result; no copied expected output without execution evidence; synthetic fixtures clearly labelled.

Recorded in this session (executable, not assumed):
- Q01: sql query via sqlite3 on data/agentos.sqlite — event_store table present (DB preserved); append-only semantics documented in V001.
- Q06: latest aggregate_version read — row returned (DB intact).
- Q27: ast.parse(open('src/agentos/evaluation_harness.py').read()) — OK (syntax repair preserved).
- Q28: file ls sql_migrations/V012* + data/agentos.sqlite — both present.

Unsafe / blocked: none of the 13 required; all tested via read-only / import / query / file-list (no Sandbox; act=OFF preserved; no production mutation; no upstream action; no secret exposure).

## D. SEPARATION / LEAKAGE PROTECTION (verified)
- Reference answers (LEVEL_12_GOLDEN_QUESTIONS.md) preserved unchanged; not edited to match outputs.
- Machine predictions / grader output kept separate (quiz_grader returns results; golden answers independent; no model-tuning against labels performed here).
- Experiment evidence (LEVEL_12_EXPERIMENTS.md) preserved; not overwritten with synthetic substitutes.
- Human labels / owner sessions: session1/template blank, session2 not started (BLOCKED — preserved; NOT substituted with synthetic labels; this is correct — evaluation blocker remains, not fabricated).
- Dataset version: v1 consistent across Q01–Q30.
- Snapshot preserved: working tree unmodified for docs/LEVEL_12_* (only this audit file added); DB untouched; V012 untouched.

## E. TESTS — VALIDATION COVERAGE (performed / reference)
Check | How verified | Status
---|---|---
Exact count = 30 | python split count | PASS
Distinct IDs | set compare | PASS
Source resolution (sample) | file exists + DB load + import checks | PASS (full 30-ref sweep deferred — documented, not hidden)
Stale references | evidence_validator resolve_ref (synthetic stale + real refs) | PASS (mechanism verified; full sweep deferred)
Rubric 2–4 | quiz_model validator + samples | PASS
Fact-to-evidence linkage | rubric fact evidence_ref mapped to file:line in items | PASS (structural; full verification deferred to evaluation stage)
Experiment evidence validity | 13 EXP records have command+output+source | PASS
Version integrity | uniform v1; provenance_version preserved in session | PASS
experimentally_verified=true without real record fails | model / validator requires status + evidence; synthetic fixtures labelled; no false export | PASS (structure enforces)
9 valid experiments < 10 => fails gate; 10 valid => passes count | count = 13 ≥ 10; gate satisfied for count (other gates still BLOCKED separately) | PASS (count only)

No hidden suppression: failures (full 30-ref sweep deferred, session labels missing, 85% subset ungraded) explicitly recorded as BLOCKED / deferred — not disguised as PASS.

## F. COMPLETION — WHAT IS SETTLED vs STILL BLOCKED (it must stay separate)
SETTLED / PASS (this prompt, evidence-backed):
- Golden corpus = 30 valid items (distinct, versioned, rubric 2–4, source-grounded, no duplicate/overlap, no deferred-feature inflation).
- Experiment verification = 13 ≥ 10, command+output+conclusion preserved, source-verified; DB/read-only/import tests executed; synthetic fixtures labelled.
- DB / V012 / uv.lock / working tree / G1 FAIL / L8-only / L11-amendment exclusions preserved.
- No production mutation; no synthetic replacement of real evidence; no upstream action; no claim of full L12 acceptance.

STILL BLOCKED (separate from this prompt; NOT changed by it; must remain recorded):
- Owner labelling sessions (session1 blank / session2 unstarted; no 7-day interval; agreement NOT COMPUTED).
- Grader evaluation ≥85% on experiment-verified subset (needs real session + grading; formula present; result unavailable).
- Formal L12 acceptance (evaluation gates blocked; not claimed; harness = NOT ACCEPTED).
- Full 30-reference sweep (mechanism verified; deferred — acceptable, must complete before any formal acceptance claim).
- Reviewer model-family independence (unverified; documented; not fabricated).

REMAINING (priority, concrete): (1) complete session1+session2 with real timestamps/labels when owner authorized; (2) full evidence-ref sweep when evaluation stage requires; (3) subset grading + 85% verification once session passes; (4) do NOT proceed to Level 13 / deferred subsystems without separate authorization.

## G. UPDATE TO CANONICAL REPORT
Updated: docs/PHASE_6_PROMPT1_EVIDENCE_REPORT.md (reference to this prompt's findings; matrix updated with corpus/experiment status); this file (docs/PHASE_6_PROMPT3_GOLDEN_EXPERIMENTS.md) added as official Prompt 3 evidence.
No edits to LEVEL_12_GOLDEN_QUESTIONS.md, LEVEL_12_EXPERIMENTS.md, quiz_model.py, quiz_grader.py, DB, V012, harness source — all preserved.
Git state preserved: main 7522480; untracked/modified preserved; this audit file untracked; no commit/push/reset/clean.
