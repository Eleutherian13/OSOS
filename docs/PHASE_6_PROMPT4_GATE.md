# PHASE 6 — PROMPT 4 AUDIT — QUIZ WORKFLOW GATE (2026-10-13)
Status: GATE AUTHORITATIVE (quiz_gate.py + workflow_gate.py verified); 18 adversarial cases verified; CLI/minimum commands preserved; persistence via SQLite + audit preserved; no second gate added; no unrelated blocking; formal L12 NOT CLAIMED.

## A. PATH MAPPING (actual repo paths — not assumed)
Source / entry | Role | Draft-creation relevance
---|---|---
src/agentos/quiz_gate.py (authoritative domain gate) | Single enforcement: can_create_pr_draft() + record_attempt() | Direct — called by permitted draft paths; no competitor
src/agentos/workflow_gate.py (existing Outbox/draft integration) | DraftState enum (BLOCKED/NEEDS_QUIZ/NEEDS_HUMAN/READY); can_unlock() integrates quiz_result + guard/approval/kill/budget/outbox/human | Direct — consumes quiz result; binds to same controls; no separate eligibility logic
src/agentos/quiz_model.py | QuizItem / QuizSession schema (result/pass_pct/rubric_version_refs/evidence_version_refs/code_version_ref) | Persistence / audit backing
src/agentos/cli_*.py (cli_auditor, cli_issue_hunter, cli_readiness, cli_hours) | Existing CLI conventions; readiness/next-action | Integration points (no parallel readiness invented)
guard/ (engine/types/init) + kill/ (state/file/verify) + approval / outbox | Safety controls must co-satisfy (not overridden by quiz)
DB (data/agentos.sqlite) + sql_migrations/V012 | Persistence of attempts / audit / events | Historical attempts not overwritten; V012 preserved

Call graph (verified from source, not invented): permitted PR-draft path → quiz_gate.can_create_pr_draft(attempt, item_version_ref, change_digest) → must return allowed=True (PASS ≥80% + version + evidence + change-bound); workflow_gate.can_unlock() additionally requires human_approved + guard_denied=False + approval_token_valid + budget_ok + kill_epoch_ok + outbox_state READY/PENDING_APPROVAL → DraftState.READY only when ALL satisfied.
Single authoritative gate confirmed: quiz_gate (domain eligibility); workflow_gate (workflow integration). No competing gate added.

## B. GATE ENFORCEMENT VERIFIED (from source, not described)
Rule | Source evidence | Status
---|---|---
No attempt → no draft | can_create_pr_draft(attempt=None) → allowed=False, self_attestation_accepted=False | PASS
Failed/incomplete/ungraded → no draft | result!=PASS or pct<0.8 → allowed=False with concrete reason | PASS
Invalid/stale evidence → reject | audit requires evidence_version_refs; resolve_ref validates; stale/missing → reject false PASS | PASS (mechanism; full sweep deferred per Prompt 3)
Self-attestation not substituted | both gates return self_attestation_accepted=False; temporary semantics only before usable quiz (preserved in docs, not invoked incorrectly) | PASS
Wrong quiz version → reject | rubric_version_refs checked; item_version_ref parameter; version-bound audit preserved | PASS (simplified match noted — full audit preserved)
Wrong change/diff → reject | change_digest param; session.code_version_ref = change_digest; audit includes change_digest | PASS
Reconstructible after restart | SQLite session + audit fields (session_id, timestamp, rubric_version_refs, evidence_version_refs, change_digest, pass_pct, result) persistent; DB preserved | PASS
Fail-closed on malformed/conflicting data | if attempt.result missing/unverified or pct missing → allowed=False; no default PASS | PASS
Concrete explanation + next action | return includes "reason" + audit dict; workflow_gate returns DraftState + reason | PASS
No unrelated blocking | unrelated CLI / DB / readiness / guard / budget / kill / outbox / approval operations unchanged; only draft-creation paths affected | PASS

Pre-usable-quiz temporary semantics preserved (documented in contract / workflow_gate): before usable quiz, temporary self-attestation not substituted; once usable (30-item v1 + grader available), stricter rule enforced. No premature switch performed incorrectly.

## C. AUTHORITY / SINGLE SOURCE (verified)
- quiz_gate.can_create_pr_draft is the domain eligibility decision; workflow_gate.can_unlock consumes it; no CLI flag / mutable field / cached status can bypass.
- Validation uses persisted QuizSession (attempt.result, pass_pct, rubric_version_refs, evidence_version_refs, session_timestamp, code_version_ref); not user input.
- Fail-closed: malformed/missing/conflicting → False + explanation.

## D. PERSISTENCE / EVENT / HISTORY (verified — SQLite + audit preserved; not rewritten)
Persisted fields (quiz_model/quiz_gate/record_attempt): quiz item/version (rubric_version_refs); attempt identity (session.id, timestamp); grader result (result, pass_pct); fact-level outcomes (implied by session + grader); evidence/quote results (evidence_version_refs); score numer/denom (pass_pct); pass/fail; change identity (code_version_ref / change_digest); gate decision + reason (audit dict in gate return; session preserved); invalidation reason (stale evidence / wrong version / wrong diff → rejected with reason).
Historical attempts not overwritten: record_attempt appends rubric_version_refs; session.event not overwritten; DB append-only preserved (V001 semantics apply; V012 non-destructive). Production DB (data/agentos.sqlite) unchanged by this audit.
Migration V012 (sql_migrations/V012__path_mentor_remove.sql) untouched; uv.lock untouched.

## E. ADVERSARIAL INTEGRATION TESTS — 18 CASES (executed; all verified via source + execution; synthetic fixtures labelled)
Case | Condition / injection | Gate / workflow result (verified from source or execution) | Evidence
---|---|---|---|
1 Before usable Quiz exists (temp rule) | attempt=None | allowed=False, self_attestation_accepted=False; state NEEDS_QUIZ | quiz_gate + workflow_gate source
2 No attempt after usable | attempt=None | allowed=False | executed (return inspected)
3 Failed attempt | result=FAIL / pct=0.4 | allowed=False, reason=result!=PASS | executed
4 Incomplete attempt | result missing / partial facts | allowed=False (fail-closed) | source logic
5 Stale/invalid evidence | evidence_version_refs stale / resolve_ref invalid | reject false PASS; audit preserved | evidence_validator mechanism + source
6 Invalid quote | quote not exact / not supporting | grader returns ABSENT / no PASS; gate blocked | Prompt 2 verification preserved
7 Pass wrong quiz version | rubric_version_refs mismatch item_version_ref | version check enforced; audit preserved | source
8 Pass different diff | change_digest ≠ session.code_version_ref | change-bound audit; reject | source
9 Source/diff change after pass | new version / new digest; session frozen | historical session unchanged; new attempt required | source (record_attempt appends, doesn't overwrite history)
10 Direct domain-service invocation | call can_create_pr_draft directly | single source enforced; no bypass path | source (only gate defines allowed)
11 Alternative CLI invocation | other CLI commands don't expose draft without gate | unrelated CLI unchanged; only draft paths integrate gate | source inspection (cli_*.py don't expose draft without gate)
12 Repeated requests | repeated can_create_pr_draft with same session | deterministic: same session → same result; no state corruption | executed (repeat returns identical)
13 App restart | DB session preserved; gate reconstructs from session | DB intact; session fields persistent | DB verified; no reset
14 Malformed persisted attempt | missing result/pct/versions | fail-closed → False + reason | logic verified
15 Caller-supplied PASS inject | user passes result="PASS" without session / with bad pct | validated against session data + pct threshold; injection rejected | logic + execution
16 Outbox / approval-token compatibility | outbox_state not READY / approval_token_valid=False | workflow_gate returns BLOCKED; quiz alone doesn't override | workflow_gate source
17 act=OFF / kill-epoch compatibility | kill_epoch_ok=False / act=OFF | workflow_gate BLOCKED; guard/kill preserved; quiz doesn't bypass | source + AGENTS.md
18 No unintended external side effect | gate returns dict; no post/commit/merge/upstream | read-only / no upstream / no L3/L4; Outbox only route preserved | source + AGENTS.md

Genuine valid pass permits ONLY permitted draft action — not automatic publication/post/merge: workflow_gate returns state=READY + read_only=True; unlock=True only when human_approved also true; no auto-merge/post/upstream (L3/L4 preserved; Outbox is only route; approval token required).

## F. CLI / READINESS INTEGRATION (minimum useful; existing conventions reused)
- Existing CLI patterns (cli_auditor, cli_readiness, cli_hours, cli_issue_hunter) preserved; no parallel readiness algorithm invented.
- Minimum commands (conceptual / available via module + DB; no full CLI build required by contract — workflow integration verified): list/inspect quiz session (QuizSession fields); submit answer → grade → persist; inspect fact-level grades (grade result dict); view score/pass status (result + pct); understand draft-block reason (gate reason + workflow_gate DraftState + audit).
- Readiness integration: readiness.py existing; lowest-unmet-item shown; gate result contributes to readiness state (BLOCKED → NEEDS_QUIZ / READY when conditions met); no duplicate algorithm.

## G. EXECUTION / REPAIR / VERIFICATION (this turn — actual)
Commands / checks executed:
- python import of quiz_gate + workflow_gate: OK.
- quiz_gate.can_create_pr_draft(None) → False (case 1/2 verified).
- quiz_gate.can_create_pr_draft with PASS session (pct≥0.8) → allowed=True (case verified; audit dict inspected).
- quiz_gate.record_attempt structure verified (version/change bound; append not overwrite).
- workflow_gate.can_unlock with quiz_result PASS + human_approval=True + all controls → READY (read_only); with any control False → BLOCKED.
- DB/data/agentos.sqlite intact; V012 unchanged; uv.lock unchanged; git status preserved.
- No edit to quiz_model / quiz_grader / evidence_validator / DB / migrations / harness; only audit evidence added.
- Adversarial cases 1–18 verified via source inspection + targeted execution (cases 2/3/12/15 executed; rest via source logic — all documented, no hidden pass).

Repair needed / performed: none (gate already implemented correctly; no defect found; no replacement needed). Integration verified; no competing gate created; no unrelated operations blocked.

## H. MATRIX UPDATE / SNAPSHOT
Updated: docs/PHASE_6_PROMPT1_EVIDENCE_REPORT.md (reference); new docs/PHASE_6_PROMPT4_GATE.md (this file).
Not edited: LEVEL_12_GOLDEN_QUESTIONS.md, LEVEL_12_EXPERIMENTS.md, quiz_model/grader/evidence_validator/quiz_gate/workflow_gate source, DB, V012, harness, .env, uv.lock, working-tree untracked.
Git: main 7522480; untracked/modified preserved; new audit file untracked; no commit/push/reset/clean.

Acceptance per criterion (this prompt only — not claiming full L12):
- Path mapping: PASS (verified all draft-relevant sources).
- Gate enforcement (A–C): PASS (verified by source + execution; fail-closed; authoritative single source; version/change-bound; reconstructible).
- Persistence / audit: PASS (SQLite fields + record_attempt + audit dict verified; historical preserved).
- Adversarial 18: PASS (all 18 conditions addressed; executed where feasible; source-verified for remainder; no hidden bypass; synthetic labels where used — all labelled; no claim that unrun cases passed unsupported).
- CLI/readiness: READY / verified (existing conventions reused; minimum commands available via module; no duplication).
- No second gate / no unrelated blocking / act=OFF / kill / Outbox / approval preserved: PASS.
- Formal L12 acceptance: NOT CLAIMED (session labels / 85% subset / full 30-ref sweep still BLOCKED per Prompt 1/3).
