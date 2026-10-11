# Canonical Roadmap Execution Plan — OSS-AgentOS v2.1 (Official 0–17)

Status: DESIGN_A_ACCEPTED_FOR_SCOPED_USE (Prompt 8 audit complete); REAL_E2E=BLOCKED (honest); Design B deferred; transition to Prompt 9 verified
Prepared: 2026-10-11
Source of truth: docs/ROADMAP_0_17_RECONCILIATION.md (4778B, verified 2026-10-11)
Crosswalk: internal labels mapped to official 0-17 (Level 8→10, 9→11, 10→12, 11→14, Auditor→16)

## 1. Verified Status Matrix (from reconciliation + source inspection)

| Lv | Component | Actual Status | Evidence / Source Check | Acceptance | Next Milestone |
|---|---|---|---|---|---|
| 0 | System Contract | ACCEPTED | AGENTS.md (26758B); guard/outbox/approval/kill-epoch verified | PASS | Preserve |
| 1 | Persistence / Event Sourcing | ACCEPTED | SQLite; append-only; migrations V000–V011; V012 trigger | PASS | Preserve |
| 2 | Mentor Project Path | PARTIAL | Schema present; DB paths/interactions/mentors=0; sources confirmed | BLOCKED — evidence missing | Gather evidence |
| 3 | Evidence Engine | PARTIAL | evidence_repo.py; event schema; DB readable; evidence=0 | BLOCKED — DB empty | Gather evidence |
| 4 | Policy + Contact Registry | IMPLEMENTED | registry/orgs/open-os-demo.yaml verified; policy BLOCKED (not fabricated) | PASS (scope) | Confirm with owner |
| 5 | Watcher | IMPLEMENTED | watch/ verified; registry watch_targets | PASS | Preserve |
| 6 | Guard / Outbox / Approval / Kill | IMPLEMENTED | guard/; approval tokens; kill_state=1; outbox=0 | PASS | Preserve |
| 7 | Kill Switch + Budget + Hours | IMPLEMENTED | cli_hours; hours_service; DB hours_log=0; L11 verified | PASS | Gather hours |
| 8 | V0 Integration | PARTIAL-ACCEPTED | Ranking engine verified; G1=FAIL blocks full | BLOCKED — G1 gate | Resolve G1 / preserve history |
| 9 | V0 Evaluation (G1) | FAIL (historical) | G1_OVERRIDE_AUTHORIZED present; NOT rewritten to PASS | BLOCKED — evaluation blocked | Preserve result; do not fabricate |
| 10 | Ranking | IMPLEMENTED | cli_rank.py; tests; 8/9/10 reports; SORT-AID | PASS (scope) | Confirm sequencing resolution |
| 11 | GitHub Client + Issue Hunter | IMPLEMENTED | cli_issue_hunter; 13/13 tests; Stage B verified; 50-issue benchmark BLOCKED | BLOCKED — benchmark missing | Confirm benchmark / evidence |
| 12 | Understanding System | PARTIAL | grader/schema; 30 golden answers / 2-session labelling; syntax errors noted; independent-family unverified | BLOCKED — benchmark/evaluation missing | Confirm benchmark / evaluation |
| 13 | Context Engine / Dossier | DEFERRED | Conditional; ripgrep sufficient; no measured bottleneck (AGENTS.md §12) | NOT STARTED | Do not start — no bottleneck |
| 14 | Sandbox | IMPLEMENTED | Stage A (integrity + prefetch) + Stage B (isolation verified); amendment adopted (L11-only); entry trigger NOT MET preserved | BLOCKED — original entry condition not met (preserved) | Preserve amendment scope |
| 15 | PR Shepherd | NOT STARTED | No verified PR/review evidence; DB interactions=0; bottleneck: evidence | BLOCKED — missing inputs | Gather PR/review evidence |
| 16 | Proposal Evidence Auditor | ACCEPTED (Design A) | 3 source files; 15/15 tests; CLI registered; DB=0 preserved; real E2E BLOCKED (honest) | PASS (scoped); BLOCKED (full E2E / semantic B) | Confirm real proposal draft / idea / size / hours |
| 17 | Production Hardening | NOT STARTED | Conditional on prior acceptance | BLOCKED — prerequisites missing | Resolve prerequisites |

## 2. Internal-to-Official Crosswalk (verified, not renamed)
- Internal Level 8 (ranking) → Official 10
- Internal Level 9 (Issue Hunter) → Official 11
- Internal Level 10 (Quiz/Reviewer) → Official 12
- Internal Level 11 (Sandbox) → Official 14 (amendment L11-only; entry trigger NOT MET; NOT expanded to full Level 14)
- Internal Level 12 (Proposal Evidence Auditor) → Official 16 (Design A verified; Design B blocked)
- Security / compliance (§13.1–§13.8) → Cross-cutting; not official Level 13 (Context Engine)
- No historical reports overwritten; no labels erased

## 3. Critical Conflicts / Gaps (from reconciliation)
- G1=FAIL preserved; ranking (Level 10) implemented before G1 passed (historical conflict preserved, not hidden)
- 50-issue benchmark (Level 11) unavailable — not fabricated
- 30 golden answers (Level 12) — evaluation prerequisites missing; syntax errors preserved
- Level 14 Sandbox: Stage A dependency downloads / volume population / hash verification — partial (manifest present; fixtures empty; docker unavailable for full verification); Stage B isolation verified
- Proposal Evidence Auditor Level 16: Design A scope verified; Design B blocked (no model provider/integration/dataset); real proposal draft content BLOCKED (honest)
- Evidence ledger (DB): evidence=0 — bottleneck for Level 8/9/10/11/15/16 evaluation (missing data, not false)

## 4. Preservation Status (verified)
- SQLite DB: preserved (evidence=0, no mutation)
- uv.lock: preserved
- G1=FAIL + G1_OVERRIDE_AUTHORIZED: preserved
- L11 PARTIAL-ACCEPTED + amendment: preserved (entry trigger NOT MET)
- Historical reports: preserved (G1, G0, L10, L11, L8)
- AGENTS.md: preserved (binding decisions intact)
- No new model provider; no secret exposure

## 5. Recommended Sequence (dependency-aware)
1. Confirm / supply proposal draft / idea / size/hours for Level 16 real E2E (blocks semantic evaluation; not blocking Design A use)
2. Confirm registry policy / evidence for Level 4 (already verified; only BLOCKED proposal_text documented)
3. Gather evidence ledger data (DB population) — prerequisite for Level 3 / 8 / 10 / 11 / 15 verification
4. Confirm 50-issue benchmark for Level 11 (do not fabricate)
5. Confirm 30 golden answers + experiment verification for Level 12 (do not fabricate)
6. Resolve G1 evaluation (historical; do not rewrite; document for Level 8 sequencing)
7. Complete Sandbox Stage A dependency verification (volume, hashes, offline execution) — only if Level 14 acceptance needed
8. Only after 1-7: consider any Design B / semantic capability authorization

## 6. Stop Conditions (must hold)
- Do NOT fabricate proposal content, evidence, mentor replies, PR activity, benchmark labels, or evaluation results
- Do NOT claim READY_FOR_IMPLEMENTATION for full semantic auditor (Design B not authorized)
- Do NOT expand Sandbox beyond amendment scope (L11-only entry trigger)
- Do NOT start Context Engine (no measured bottleneck)
- Do NOT start Policy extractor (scale < 12)
- Do NOT reset DB or discard historical reports

## 7. Notes / Caveats
- Design A (Probabilistic Auditor, deterministic-only) accepted for scoped use
- Design B (semantic accuracy / mentor judgment) blocked correctly per approved limitation
- Real E2E remains BLOCKED until proposal draft content available — this is correct and must stay visible
- All dates reflect actual artifact timestamps (11-10-2026 for L11/Plan docs; 10-10 for earlier work)
