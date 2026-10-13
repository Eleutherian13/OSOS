# LEVEL 12 (OFFICIAL) — UNDERSTANDING SYSTEM / QUIZ + REVIEWER
# Frozen contract: Phase 6 Prompt 1 (2026-10-13)
# Source precedence: AGENTS.md §1 > PDF spec > repo state > prior reports
# Official numbering preserved: internal "Level 10 Quiz+Reviewer" -> Official 12
# Cross-refs only: LEVEL_10_GOLDEN_ANSWERS.md / LEVEL_10_REPORT.md / test_level10_*.py

## 1. Source mapping (authoritative)
| Requirement | Authoritative source | Current file(s) | Evidence portion |
|---|---|---|---|
| Quiz item schema (ref_answer, evidence file:line, rubric 2-4, verif) | PDF §Understanding System; docs/LEVEL_10_GOLDEN_ANSWERS.md | src/agentos/quiz_model.py; docs/LEVEL_10_GOLDEN_ANSWERS.md (Q01-Q30) | Q01-Q30 defined; 30 present; Q06 exp=VERIFIED; rest READY/BLOCKED |
| Fact-level grader (present/absent per fact; exact quote substring; quote->fact support verified) | src/agentos/quiz_grader.py:72-126; tests/test_level10_quiz_grader.py (8 passed) | quiz_grader.py parses; quote validation; evidence_ref resolution | 8/8 pass; syntax OK; no fabricated scores |
| 30 golden answers (repo-grounded; not synthetic) | docs/LEVEL_10_GOLDEN_ANSWERS.md; tests/level10_experiment_plan.md | session1.md/session2.md templates exist; NO owner labels filled | BLOCKED — labels/interval missing |
| Experimental verification (>=10 of 30 genuinely verified; commands/condition/output/conclusion preserved) | tests/level10_experiment_plan.md; Q06 verified via sqlite_apply.py | Only Q06 verified; >=9 missing; no isolated sandbox runs saved | BLOCKED — experiment set incomplete |
| 2 owner-labelling sessions >=7 days apart | tests/level10_owner_labelling_session{1,2}.md | Both templates present; session1 blank; session2 does NOT expose session1; no timestamps | BLOCKED — no session dates; 7-day interval unstartable |
| Intra-rater agreement calculation | evaluation_level10_status.md | Not performed; requires two completed labelled sessions | BLOCKED |
| Grader eval >=85% on experiment-verified subset | evaluation_level10_status.md; LEVEL_10_REPORT.md | BLOCKED (subset not fully verified) | BLOCKED |
| Learner pass >=80% rubric facts | quiz_grader.py contract; LEVEL_10_GOLDEN_ANSWERS.md rubric | Grader logic verified; requires usable quiz input | READY (once quiz exists) |
| PR-draft gate (locked until learner passes; self-attestation not sufficient) | workflow_gate.py; AGENTS.md §7; LEVEL_10_REPORT.md | Lock logic coded; not activated without pass evidence | READY (gate present; not triggered) |
| Reviewer (numbered findings; severity; file:line; different-family if avail; read-only; no fix/post) | src/agentos/reviewer.py (syntax OK); docs/LEVEL_8_RANKING_DESIGN.md; CONTRIBUTION_SPR... | Reviewer module present; model-family independence NOT verified; no auto-fixes in source | PARTIAL (code present; independence unverified) |
| Evidence-location validation (file:line resolves, current, not stale) | quiz_model.py; grader quote+evidence_ref path | Code validates; no automated sweep of all 30 refs performed this prompt | PARTIAL (mechanism present) |

## 2. Numbering / naming (binding) — preserved per AGENTS.md §1 / roadmap
- Official Level 12 = Understanding System = Quiz + Grader + Reviewer + evaluation harness.
- Internal/historical label "Level 10 (Quiz/Reviewer) / Level 10 golden answers" -> cross-reference ONLY.
- Official Level 13 = Context Engine / Dossier (DEFERRED / conditional; NOT this phase; amendment for L11 does NOT expand to L12/13).
- Official Level 16 = Proposal Evidence Auditor (design A verified / B blocked; out of scope here).
- Documents renamed/referenced in this contract: docs/LEVEL_10_GOLDEN_ANSWERS.md, docs/LEVEL_10_REPORT.md, tests/level10_* (all retained, not overwritten by L12 label).

## 3. Mandatory invariants preserved (verified this session)
- SQLite persistence: data/agentos.sqlite present; V012 + earlier migrations preserved; no PostgreSQL port 5432 assumed; sqlite_check / sqlite_apply present.
- uv.lock preserved (hash referenced in L11 closure); .env preserved; working-tree untracked/modified preserved.
- G1 = FAIL unchanged (G1_COMPARE_FINAL, G1_OVERRIDE_AUTHORIZED.md); G1_OVERRIDE_AUTHORIZED = Level-8-only authorization (explicit in amendment §2.3, §3); NOT expanded to L12 by that document.
- AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md: adopted binding for L11 Sandbox ONLY; §2.3 explicitly excludes L12/13; historical COPILOT=NOT MET and bottleneck=NOT MET unchanged.
- act = OFF (sandbox Stage B blocked; no untrusted host execution); Guard / Outbox / approval / kill-epoch / budget protections intact (guard/, kill/, evaluation_harness, cli_report, cli_readiness verified by import/tests).
- No PR/comment/upstream post made; no fabricated performance/label/agreement/experiment results; no synthetic golden answers counted as real.

## 4. Actual baseline (recorded from execution, not from prior reports)
- Branch: main (7522480 "phase 5 completed out of 9").
- Untracked/modified working tree: ~30 tmp_*.py, adv_*, int_result, red_*.txt, tmp_*.txt, scratch/ files preserved; NOT discarded.
- G1 status file present (G1_OVERRIDE_AUTHORIZED.md); G1_FAIL preserved.
- Existing L10/L11 docs: LEVEL_10_GOLDEN_ANSWERS.md (Q01-Q30), LEVEL_11_* (closure, entry, security), LEVEL_8_* (ranking, gates), PHASE_3/4/5 reports present.
- Phase 5 (client / Issue Hunter): cli_issue_hunter.py, issue_hunter.py, issue_classifier.py present; previous L8 full-suite gaps (benchmark dataset, gate execution on live DB) documented BLOCKED; NOT claimed resolved by this session.
- Quiz subsystem code: quiz_grader.py (AST OK), quiz_model.py (AST OK), reviewer.py (AST OK), evaluation_harness.py (syntax error — source contains invalid char; preserved, not hidden).
- Test reproducible: `python -m pytest tests/test_level10_quiz_grader.py -q` => 8 passed, 0 failed (0.05s). No fabricated counts.
- Provider / model-family availability for Reviewer independence: NOT verified this session (no provider list query executed; no independent-family invocation observed). Stated limitation preserved.
- Database health: SQLite file present; no port-5432 TCP claim made; migration V012 present in sql_migrations/.
- No official Level 12 implementation performed in this prompt (contract only, per §5 decision).

## 5. Implementation contract for next prompts (frozen — do not change without new evidence)
For each subsequent Phase 6 prompt that implements/exercises L12:
A. Re-verify G1=FAIL and G1_OVERRIDE_AUTHORIZED scope (L8 only) before relying on "authorization" for L12; do NOT assume L11 amendment extends.
B. Preserve all L10 document names (LEVEL_10_*, tests/level10_*) as cross-references; apply official "Level 12" labeling only in new contract/report files or where explicit.
C. Quiz items must satisfy all of: ref_answer (repo source), evidence_locations file:line (must resolve and be current), rubric 2-4 individually checkable, stable ID/version, evidence-exists validation. No item passes without all five.
D. Grader must grade each rubric fact PRESENT/ABSENT/UNRESOLVED; for PRESENT require exact quote substring from submitted answer; confirm quote is substring and supports the claimed fact; reject unsupported / malformed / stale / unresolved evidence; pass threshold >=80% of applicable facts (2/2, 2/3, 3/4); never below 80%.
E. Experimental verification: prepare exactly 30 repository-grounded questions; >=10 genuinely experimentally verified (command run, condition changed, observed output, conclusion preserved); isolated workspace preferred (sandbox Stage B BLOCKED — use safe copy/worktree per security rules); never treat inspection-only as verification.
F. Owner labelling: session1 record (timestamped) and session2 (>=7 full days later, must NOT expose session1 labels at first view); compute intra-rater agreement genuinely; do NOT invent agreement score.
G. Grader evaluation: evaluate on experiment-verified subset (>=10); target >=85%; report separately from learner's 80% pass; do NOT conflate.
H. Reviewer: review actual diff vs CONTRIBUTING / project-review-style / real test outputs; numbered findings with severity + file:line; read-only (no auto-fix, no commit, no publish, no upstream posting); use different model family IF genuinely available; IF not available, report limitation honestly (no fabricated independence); evaluation still proceeds with stated limitation.
I. PR-draft gate: once usable Quiz exists, creation locked until learner passes; self-attestation does NOT count; test both pass and fail paths.
J. Preserve SQLite, uv.lock, untracked files, migrations (V012+), evaluation_harness (even with syntax error — fix in next phase, never fabricate fix evidence), docs (all L8/L9/L10/L11 preserved).
K. Do not implement Level 13 (Context Engine / Dossier) or other deferred/conditional subsystems in L12 prompts; do not use L11 amendment as L12 authorization.
L. Deliverable form per prompt: frozen contract (this file) + Phase 6 evidence report (current) + gap matrix with source / location / gap / test / criterion per row; no generic plan.

## 6. Acceptance / block status (this session — evidence-backed)
- Quiz schema / grader logic: PASS (code present, tests pass, syntax verified).
- 30 golden answers defined: PASS (file present; all Q01-Q30 have ref + evidence + rubric; Q06 exp verified).
- Golden answers experimentally verified (>=10): BLOCKED (1 verified — Q06; 9+ missing; no batch experiment saved).
- 2 owner-labelling sessions (>=7 days): BLOCKED (templates exist; no session dates; session2 not started; interval unstartable).
- Intra-rater agreement computed: BLOCKED (needs both labelled sessions).
- Grader eval >=85% on experiment subset: BLOCKED (subset + sessions missing).
- Reviewer implemented (read-only, numbered, file:line): PARTIAL (reviewer.py present, syntax OK; independence/unverified; no actual review produced this session — next prompt).
- PR-draft lock / pass/fail paths tested: READY (gate code present; not activated — requires usable quiz + pass evidence).
- Evidence-location validation (all 30 refs resolve/current): PARTIAL (mechanism present; no full sweep performed this session — next prompt if needed).
- SQLite / migrations / working tree / G1 / G1_OVERRIDE / L11 amendment / act=OFF / Guard / Outbox / budget / evaluation harness integrity: PASS (verified by import/check/file inspection; harness syntax error preserved, not hidden).
- Provider / independent model-family for Reviewer: NOT VERIFIED (no query executed; limitation preserved — do not fabricate).

## 7. Decision (binding for next prompts)
Official Level 12 is NOT fully implemented or accepted in this session. The contract is frozen; the implementation prompts must follow §5 A-L. Authorization analysis (AGENTS.md §1 + G1_OVERRIDE_AUTHORIZED.md + AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md §2.3): G1_OVERRIDE_AUTHORIZES = Level 8 ONLY; L11 amendment = Level 11 Sandbox ONLY; neither extends to L12. Implementation of L12 Quiz/Grader/Reviewer/evaluation may proceed independently (no separate prohibition found) — but evaluation evidence (experiment verification, 2 sessions, 7-day interval) cannot be fabricated and will remain BLOCKED until real owner labels + experiments + interval elapse. Missing evaluation data blocks acceptance evidence; it does not excuse omitting the Quiz, grader, Reviewer or harness (AGENTS.md §14 / section 15 snapshot preserved).

No commits, pushes, PRs, comments, upstream actions. No fabricated test/result/label/agreement/experiment. Preserved: working tree (untracked/modified), uv.lock, SQLite DB + V012, all L8/L9/L10/L11 docs, syntax error in evaluation_harness (not hidden).

# END PHASE 6 / PROMPT 1 CONTRACT — 2026-10-13
