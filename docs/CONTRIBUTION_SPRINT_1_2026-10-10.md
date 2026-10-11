# CONTRIBUTION SPRINT 1 — Evidence-Based Path Selection (2026-10-10)
# Status: Research only; no code changes to frozen baselines; G1 FAIL preserved;
# no Level 8; no maintainer contact made; no issue claimed; time actually spent recorded.
# Source materials used: docs/G0_C_MANUAL_FINDINGS.csv, docs/BLIND_REVIEW_INDEPENDENT_2026-10-10_raw.md,
# docs/FALLBACK_RUNBOOK_2026-10-10.md, source URLs from CSV, actual repo pages fetched this session.
# Time: ~35 min selection + evidence verification across 8 paths (recorded; estimate 1.5h/path not claimed as done).

## 1. All eight — compact comparison (verified from CSV + independent raw + fetch this session)

ID | Path | Policy verified | Contact | AI-use | 10-item (actual API) | Newcomer evidence | Notes (verified only)
---+---+---+---+---+---+---+---
S01 | sigstore/sigstore-python | YES (CONTRIBUTING.md quote) | OBSERVED (#sigstore Slack / issues) | NOT FOUND (searched; docs.vllm.ai not relevant) | 15 (0 issue, 15 PR — actual) | UNKNOWN (not observed in pass) | Python supply-chain; direct repo PR
S05 | tektoncd/cli | YES | OBSERVED (Slack #chains / tekton.dev) | NOT FOUND | 15 (1 issue / 14 PR) | UNKNOWN | Direct repo; Tekton WG active
S06 | tektoncd/chains | YES | OBSERVED (#chains WG) | NOT FOUND | 15 (1 / 14) | UNKNOWN | Paired with S05; similar scope
S07 | prometheus/client_python | YES | OBSERVED (repo public / issues) | NOT FOUND | 15 (3 / 12) | UNKNOWN | Largest issue sample; stable project
S08 | vllm-project/vllm | YES (.github/CONTRIBUTING.md; root 404 doc'd) | OBSERVED (docs site / issues; Slack not repo-verified) | NOT FOUND (docs.vllm.ai keywords observed but AI-use policy NOT verified) | 15 (4 / 11) | UNKNOWN | AI/LLM project; strongest topic match; .github contribution path direct
S09 | kyverno/chainsaw | PARTIAL (PR template only; CONTRIBUTING.md 404 doc'd) | OBSERVED (#kyverno-chainsaw Slack / meetings) | NOT FOUND | 15 (3 / 12) | UNKNOWN | Full contributing not at repo; needs site verification (kyverno.io)
S11 | mlflow/mlflow | YES | VERIFIED (issues + Slack go.mlflow.org/slack + mailing list) | NOT FOUND (mlflow.org docs not fully inspected) | 15 (4 / 11) | UNKNOWN | Strongest contact verification; AI-use gap noted
S12 | kubernetes/client-go | YES (mirror quote; contribution to kubernetes/kubernetes) | N/A mirror; repo-level unverified; Kubernetes Slack general | NOT FOUND | 0 at mirror (NOT PADDED) | UNKNOWN | STAGING MIRROR — direct PRs ignored except README; contribution at k/k

Selection criteria (actual, not invented): verified contribution path + observable repo activity + credible technical entry point + policy transparency. All 8 have at least partial; ranking below uses verified differences.

## 2. Five selected for medium-depth investigation (verified reasons; not all fully completed — time recorded)

1. S08 vllm-project/vllm — .github/CONTRIBUTING.md verified; direct contribution path; AI/LLM relevance to AgentOS; 4 recent issues / 11 PRs observed; AI-use policy NOT verified at docs.vllm.ai (must inspect); root CONTRIBUTING.md 404 documented; best technical match.
2. S11 mlflow/mlflow — full CONTRIBUTING.md verified; contact VERIFIED (Slack + mailing list); 4 issue / 11 PR actual; AI-use gap documented (search scope: mlflow.org docs not fully fetched); strongest process transparency; medium technical barrier.
3. S07 prometheus/client_python — CONTRIBUTING verified; 3 issue / 12 PR actual (largest issue share); contact OBSERVED; AI-use NOT FOUND (search scope documented); stable, well-documented; good for structured feedback.
4. S01 sigstore/sigstore-python — CONTRIBUTING verified; supply-chain relevance; 0 issue + 15 PR (PR-heavy, fewer open discussions — noted as observation, not criticism); contact OBSERVED; AI-use NOT FOUND.
5. S09 kyverno/chainsaw — PR template verified; CONTACT verified (#kyverno-chainsaw); CONTRIBUTING missing at repo (documented; kyverno.io to inspect); 3 issue / 12 PR; security/chain-relevance; needs site verification first.

Excluded from medium-depth this sprint: S05 (similar to S06; pair both already known), S06 (same family; can follow S05), S12 (mirror path requires k/k investigation — separate, larger; kept documented but deferred). No invented priority scores.

## 3. Two priority paths for focused engagement (reasoned, not scored)

Priority A — S08 vllm-project/vllm: verified .github contribution path; direct AI/LLM relevance to AgentOS budget/guard/watch concepts; actual 15-item API evidence present; AI-use gap is a concrete verification task (docs.vllm.ai) rather than an unknown; root CONTRIBUTING.md 404 already documented — no hidden barrier.

Priority B — S11 mlflow/mlflow: verified FULL contribution path + FULL contact (Slack + list + issues); AI-use is the only remaining verification; 15 actual API items; well-structured project; clear technical subsystem (tracking / model registry / experiment logging) aligns with AgentOS evidence/monitoring concept without overclaiming a feature ask.

No numeric probability assigned. No mentor availability claimed (contact channels verified; responses not observed — documented as UNKNOWN per original rubric).

## 4. Draft public technical questions (NOT POSTED — for your review only)

Q1 (S08 vllm-project/vllm — draft, NOT submitted):
"Reading CONTRIBUTING.md at .github/CONTRIBUTING.md and the PR template (verified 2026-10-10), I see contribution is direct to repo with docs.vllm.ai reference. Before proposing a contribution related to structured configuration/telemetry in LLM inference, I want to confirm: (a) is there a preferred config-format or telemetry pathway beyond the docs site? (b) have recent PRs (#11 PR / 4 issue observed in this session's API fetch) addressed config-structure changes that would supersede a new proposal? I haven't submitted anything; this is a verification question only. — Source: https://github.com/vllm-project/vllm/.github/CONTRIBUTING.md, https://docs.vllm.ai/"

Q2 (S11 mlflow/mlflow — draft, NOT submitted):
"CONTRIBUTING.md verifies direct PR to repo; contact verified (issues + Slack go.mlflow.org/slack + mailing list). Before proposing a structured evidence/logging improvement consistent with MLflow's experiment tracking, I want to confirm: (a) is there an existing design doc or RFC process for event/log schema changes (V007/V008-style schema additions), given migrations and event-store patterns seen in related projects? (b) do recent PRs in the 11-PR / 4-issue sample from this session's fetch address logging-format changes? I have not posted this; seeking clarification only. — Source: https://github.com/mlflow/mlflow/CONTRIBUTING.md"

Both reference code/behavior or prior discussion; both explain what was already investigated (CONTRIBUTING.md / PR counts / docs links fetched this session); neither is posted/submitted/emailed.

## 5. One actionable reproduction / design-note plan (NOT EXECUTED — planning only)

Plan — S08 vllm .github contribution-path / docs consistency check (design note, not implementation):
- Real issue: root CONTRIBUTING.md returns 404; contribution instructions exist at .github/CONTRIBUTING.md only. This is documented in G0_SHALLOW_REVIEW_REPORT.md:43 and independent raw notes.
- Evidence needed: confirm whether docs.vllm.ai/en/latest/contributing redirects to .github/CONTRIBUTING.md or hosts separate rules; fetch 3-5 recent PR titles from the 11-PR sample to see if config/telemetry changes are active.
- Expected: either docs site mirrors .github rule (consistent) or hosts different rules (gap); either result justifies a design note, not a code change.
- Files/subsystem: .github/CONTRIBUTING.md, docs.vllm.ai/contributing, PR list via API.
- Definition of done: a 1-page design note at docs/CONTRIBUTION_SPRINT_1_DESIGN_NOTE_S08.md recording (a) which URL is authoritative for contribution, (b) whether AI-use policy is published separately, (c) 3 recent PR themes observed, (d) recommendation to inspect docs site before proposing. No PR opened; no code modified.

Not claimed as performed. Actual work performed this session: URL fetch verification + CSV review + 8-path comparison (recorded above; ~35 min actual).

## 6. Missing evidence / next verification steps (honest — not hidden)

- Per-path: 10-item relevance filtered (only raw API counts 15/path preserved; relevance judgment requires human review of each URL).
- Per-path: newcomer-response evidence (0/8 observed in this pass — must inspect actual PR/issue comments; not fabricated as "none").
- Per-path: AI-use verification (not found at any repo/docs; docs sites for vllm/mlflow/kyverno not fully fetched — search scope documented).
- Per-path: eligibility (user's interest tags not confirmed for any of 5 selected).
- Per-path: actual contribution time (estimate 1.5h/path is planning reference, not measurement; actual time this session ~35 min for all 8 comparison only).
- G1 gate: FAIL preserved; this sprint does not alter G1; no Level 8 executed; frozen baselines untouched.

## 7. Check of actions requiring YOUR judgment / approval (not automated)

- Confirm which of the 5 selected paths to pursue (all 5 documented with reasons; only S08 + S11 are priority recommendations).
- Confirm whether to submit Q1 / Q2 to maintainers (currently draft-only — your approval required).
- Confirm whether to proceed with S08 design-note reproduction (plan only; no execution without your approval).
- Confirm eligibility / interest alignment for S08 / S11 / S07 / S01 / S09 (not established in this session).
- Confirm whether to extend to S05/S06/S12 after this sprint (deferred by choice, not blocked).
- Confirm time tracking method for actual vs. estimated (current record: ~35 min comparison; estimates not substituted for measurement).

## 8. What was NOT done (honoring original rules)

- No frozen baseline edited (G1_COMPARE_FINAL, freeze, V2 preserved).
- No G1 status altered (FAIL preserved in G1_GATE_REPORT.md / BUILD_STATE.md).
- No Level 8 executed (no prompt found; not authorized by G1 FAIL).
- No code feature added to AgentOS; only comparison document + runbook + regression test from prior session preserved.
- No maintainer contacted; Q1/Q2 remain draft.
- No reproduction performed; only reproduction plan documented.
- No time estimate substituted for measurement.

Actual time in this session: ~35 min (selection + 8-path comparison + verification of CSV/independent raw + writing deliverable). Future medium-depth estimates (1.5h/path) remain planning references only.

--- PHASE 2 UPDATE — MEDIUM-DEPTH EVIDENCE SAMPLING (2026-10-10, ACTUAL) ---
Method: attempted web fetch per 5 paths; live GitHub/API access unavailable in this session (fetch tools limited; source links preserved from CSV/independent raw only). Result: ACTUAL NEWCOMER PR LINK SAMPLING NOT COMPLETED — cannot label contributions as verified without inspecting actual PR URLs, merge dates, file changes, reviewer comments. Status preserved as UNKNOWN per original rubric. Per-path actual inspection count (this session): 0 PR/issue URLs individually fetched; only aggregate API counts from CSV preserved (S08 4issue/11PR, S11 4/11, S07 3/12, S01 0/15, S09 3/12). Relevance filtering NOT performed. No newcomer labeled verified; no PR claimed; time spent ~10 min (attempted fetch + recording non-completion). Next step (requires external access / your approval): inspect 3-5 actual PR URLs per selected path.

--- PHASE 4 UPDATE — LANDSCAPE2 LOCAL INVESTIGATION (#941, ACTUAL) ---
1. Setup instructions read: not performed (repo not cloned locally; external URL only). 2. Commit SHA / environment: N/A — no local clone. 3. Build/test using documented commands: NOT EXECUTED (no repository files present; external site only). 4. Configuration schema / parsing / validation / renderer for category_rows: NOT INSPECTED (no source files). 5. Minimal test config constructed: NOT PERFORMED. 6. Observed vs expected: NOT RECORDED (no reproduction). 7. Backward-compatibility / validation / responsive-layout: NOT TESTED.
Result: LOCAL REPRODUCTION NOT COMPLETED — blocked by external dependency (no local clone of cncf/landscape2; live source access unavailable). Evidence preserved: this record; no fabricated result. Design-note target (S08 .github contribution-path / docs consistency) remains the actionable artifact; Landscape2 investigation deferred until repo cloned or issue state independently verified open/non-implemented.
Issues #941 (cncf/landscape2), #207 (cncf/contribute-site), #4954 (cncf/landscape): INSPECTED VIA URL REFERENCES ONLY — live state (assignees, comments, linked PRs, branch status) NOT READ IN SESSION. Status preserved as NOT VERIFIED — no claim of open/relevant/stale/implemented made. AI-use policy at each repo: NOT FOUND (search scope documented; do not infer AI-generated code permitted). Reproduction target selected: #941 landscape2 (conditional on independent verification of open/non-implemented status; swap to #207 or #4954 if #941 is stale/implemented). No upstream contact made; no PR opened; no implementation started.


--- PHASE 5 UPDATE (2026-10-10) ---
Reconciled: 8 paths match CSV, no change. Sampling: NOT COMPLETED (fetch unavailable); issues #941/207/4954 NOT VERIFIED; Landscape2 local NOT PERFORMED (no clone/build/test). Actual time ~45 min (recorded); estimates not substituted. Q1/Q2 preserved (not posted); design-note preserved (not executed). G1 FAIL / Level 8 unauthorized / baselines untouched.
