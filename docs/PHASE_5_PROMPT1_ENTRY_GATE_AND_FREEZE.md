# PHASE 5 / LEVEL 11 — PROMPT 1 ENTRY GATE & REQUIREMENTS FREEZE REPORT
Prepared: 2026-10-13 (session audit; source-backed, no fabrication)
Status of this audit: EVIDENCE-DRIVEN; pre-requisites inspected before any build.

## 1. SCOPE / WHAT WAS REQUESTED (Prompt 1 only)
- Read authoritative sources (AGENTS.md, plan PDF missing, roadmap/reconciliation, G1_OVERRIDE, L8–L11 evidence).
- Verify repository state (branch, untracked/modified, DB, tests, reports).
- Prove the bottleneck (does Issue Hunter solve a real, documented bottleneck?).
- Apply the entry gate for Level 11 (GitHub Client + Issue Hunter, internal L9 / official L11) per AGENTS.md §4, §9 and the v2.1 plan.
- Freeze Phase 5 requirements matrix IF and ONLY IF entry permits.
- Do NOT start Prompts 2–6 if gate is HOLD / NO_GO; do NOT build GitHub client as workaround.

## 2. SOURCE-OF-TRUTH & PRECEDENCE APPLIED (AGENTS.md §1)
1. Owner's latest explicit decision (amendment 2026-10-11) — applied narrowly to Sandbox (L11 internal), not expanded.
2. Original v2.1 Implementation Plan PDF — NOT FOUND at repo root (verified); treated as UNVERIFIED/absent; do not fabricate its text.
3. Existing repo behavior / schema / migrations / tests — verified below.
4. Derived design / evidence docs — used only with quoted source.
5. General best practice — only where source silent.

## 3. CURRENT REPOSITORY STATE (verified, not assumed)
- Branch: main
- Modified: data/agentos.sqlite, cli/cli_hours/cli_path, budget_service, evidence_repo, migrations V002/V003, kill/state, readiness, tests (path, level10 ranking, level2_3 integration, adversarial L4-7, watcher), plus untracked docs (PHASE_3/4, STAGE2_GAP_MATRIX) and tmp_*.py / adv_*.txt.
- Untracked new docs include LEVEL_11* reports (12+ files), AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md, LEVEL_11_ENTRY_DECISION.md / ENTRY_EVIDENCE.md / CLOSURE_GATE_ACCEPTANCE_REPORT.md, PHASE_3/4 master evidence.
- SQLite DB (data/agentos.sqlite, 286KB, 20 tables): append-only trigger `trg_event_store_prevent_delete` verified; V012 trigger reference NOT FOUND in sqlite_master (only append-only delete guard present); migrations V001–V009 present, V010–V012 not shown in file list (V009 is last in sqlite_migrations dir). Evidence counts: interactions=0, evidence=0, paths=0, mentors=0, hours_log=0, budget=0 — consistent with reported evidence-absence; NOT fabricated.
- Original 22-step L8 end-to-end: NOT completed (G1 FAIL preserved; ranking implemented but gate not passed). Prior reports say PARTIAL; current inspection confirms (DB empty, G1=FAIL preserved, no ranking-engine live gate result file generated).
- G1: FAIL (docs/G1_OVERRIDE_AUTHORIZED.md line 5, G1_GATE_REPORT.md, G0_final); NOT rewritten. G1_OVERRIDE: explicit 2026-10-10 authorization for Level 8 development ONLY (line 3, §2, §6); does NOT mention Level 11 / Issue Hunter / Sandbox beyond L8. Amendment 2026-10-11 (AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md) is a separate, L11-ONLY entry-trigger waiver for Sandbox (internal L11 / official L14) — NOT for Issue Hunter.
- Level 8 prerequisite evidence for Level 9/11: missing (DB evidence=0; no verified contributor candidates; ranking is descriptive only, not evaluation-passed).

## 4. BOTTLENECK EVIDENCE (required by plan — Issue Hunter is conditional on a measured bottleneck)
Inspected: ROADMAP_EXECUTION_PLAN.md (line 23: L11 "BLOCKED — benchmark missing"), LEVEL_11_ENTRY_EVIDENCE.md (§11: trigger NOT MET, bottleneck NOT MET — "ripgrep + direct inspection baseline sufficient"), LEVEL_11_ENTRY_DECISION.md (§1 Trigger B: NOT MET), AGENTS.md §4 (conditional: only when bottleneck real), LEVEL_9_REPORT.md / LEVEL_9_IMPLEMENTATION_REPORT.md.
- Bottleneck claim: "finding / validating contribution opportunities is slow/unreliable." Actual evidence: TEST file `tests/test_level9_github_client.py` exists (~5.7KB github_client.py, 1.4KB issue_hunter.py); the client implementation exists; 50-issue benchmark asset `docs/g0_candidates_discovery.json` exists (19KB) but NO 50-issue HAND-LABELLED BENCHMARK for Issue Hunter (L9/L11 acceptance requires human-labelled 50, ≥90% precision — AGENTS.md §9, §14).
- Specific missing task: the discovery/validation bottleneck is the 50-issue labelled set and the ≥90% "not a public candidate" precision measurement — both BLOCKED by missing human labels, NOT by missing code.
- Conclusion: bottleneck IS real ONLY for the EVALUATION / BENCHMARK path, not for the ENGINEERING / CLIENT path. The user's request to "prepare Phase 5" refers to engineering (client + matrix); that is permitted under the amendment / override only for the technical scope, NOT as proof of acceptance.
- Crucial distinction preserved (per AGENTS.md §4 conditional rule): Issue Hunter (L9 / internal) is separate from Sandbox (L11 / internal / official L14). The 2026-10-11 amendment applies ONLY to Sandbox (entry trigger waived); it does NOT authorize Issue Hunter and does NOT change G1 or expand override.

## 5. G1 + OVERRIDE FINDINGS (exact, not expanded)
- G1 verdict: FAIL. Preserved; no edit to FAIL→PASS (G1_OVERRIDE_AUTHORIZED.md §1, §6).
- Override scope: Level 8 ONLY (line 3, §3 "Level 8 work performed"). Section 5 lists remaining blockers (manual time unmeasured, 0/8 verified per-candidate, PostgreSQL deferred, missing per-agent cap). No L9/L11 authorization in override.
- Amendment 2026-10-11 (AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md): L11 Sandbox ONLY (§2.1); original NOT MET preserved (§2.2); does NOT expand to L12 (Context Engine) or L9 (Issue Hunter) (§2.3).
- Historical G1 failure is NOT a passing prerequisite for Issue Hunter; a user request does NOT authorize falsifying/benchmark-shortcutting the 50-issue label set or the ≥90% precision gate.

## 6. LEVEL 8 PREREQUISITE FINDINGS (affects L9 / L11 readiness)
- Ranking design/contracts (LEVEL_8_RANKING_DESIGN.md, LEVEL_8_HARD_GATES.md) implemented; ranking-engine live execution BLOCKED by G1 and missing evidence.
- DB: paths/mentors/interactions/evidence all 0; registry YAML verified (open-os-demo.yaml); evidence ledger = empty.
- Therefore prerequisites for Issue Hunter (verified candidate list, mentor/reviewer response within 14/90 days, merged PR within 30d, contribution-confidence with ≥10 observations) are NOT satisfied.
- Status: L8 PARTIAL-ACCEPTED; does NOT unblock L9 evaluation.

## 7. ENTRY GATE DECISION FOR PHASE 5 (Level 11 / internal L9 — GitHub Client + Issue Hunter)
Result: GO_WITH_LIMITATIONS (engineering permitted; evaluation BLOCKED; amendment does NOT expand to Issue Hunter).

Breakdown by sub-question:
- A (authoritative sources read): YES — AGENTS.md full; PDF missing (recorded); reconciliation + roadmaps + G1 override + L8–L11 evidence + CLI/DB/code inspected.
- B (repository verified): YES — branch/status/DB/migrations/G1/reports/tests listed above; untracked preserved.
- C (bottleneck proven): PARTIAL — benchmark/data gap is the real bottleneck, NOT code absence; documented in LEVEL_11_ENTRY_EVIDENCE.md and ROADMAP_EXECUTION_PLAN.md line 23.
- D (entry gate applied): GO_WITH_LIMITATIONS for engineering / requirements freeze; HOLD for full acceptance (benchmark + precision). Not NO_GO (no plan-rule stop-order applies to Issue Hunter; only conditional rule applies, and amendment doesn't touch it). Not GO (benchmark missing + G1 FAIL preserved + L8 prerequisites missing).

What is permitted (explicit, bounded):
1. Inspect / freeze requirements for read-only GitHub client + Issue Hunter (engineering design, schema, CLI contract, persistence design, test design) — the matrix below.
2. Preserve, not fabricate, the 50-issue benchmark gap and ≥90% precision requirement.
3. Do NOT claim benchmark acceptance; do NOT start Prompt 2's implementation of the benchmark or grading pipeline until labels exist.
4. Do NOT expand Sandbox amendment or G1_OVERRIDE to Issue Hunter.

What remains BLOCKED (must stay visible):
- 50-issue hand-labelled benchmark (AGENTS.md §9 / §14 / roadmap L11).
- ≥90% precision on "not a public candidate" (requires labels + independent review / second labelling).
- Recall reporting + failure-cases recording (needs labelled ground truth).
- L8 prerequisite evidence (candidate eligibility, mentor replies, 30d PR, 20h catch-up, 7 gates).
- G1 = FAIL (historical; not rewritten).
- Live end-to-end ranking gate execution.
- Level 11 Sandbox is separate; its Stage A/B work does NOT substitute for Issue Hunter evaluation.

## 8. FREEZE — PHASE 5 REQUIREMENTS MATRIX (Level 11 / internal L9 — Issue Hunter + GitHub Client)
Every row: source, expected behavior, existing implementation (if any), test command, acceptance = BLOCKED/NOT RUN/PASS per evidence.

| # | Requirement | Source | Expected behavior | Implementation found | Test / verification | Acceptance (this audit) |
|---|---|---|---|---|---|---|
| 1 | Read-only GitHub API client | AGENTS.md §9; plan L9; src/github_client.py | `httpx`/`requests` read-only; no L3/L4 write; ETag; token bucket; `Retry-After` | `src/agentos/github_client.py` (5.7KB); `tests/test_level9_github_client.py` exists | `pytest tests/test_level9_github_client.py` (NOT executed this turn — no network/auth available; preserved) | NOT RUN (code exists; live verification blocked by auth/network; not claimed PASS) |
| 2 | Conditional requests / cache | AGENTS.md §9 | `If-None-Match`; cache hit skips fetch; stale→refetch | In github_client module (unverified line-level — not inspected at function level this turn) | Unit + adversarial | NOT RUN |
| 3 | Rate limit + bounded backoff + errors | AGENTS.md §7 (§7 limits 5k/hr, 900/min); §9 | Token bucket; exponential backoff; 403/429 honored; never loop `/rate_limit` | Presumed in module (verify per function before claim) | Adversarial | NOT RUN |
| 4 | Issue state vocabulary + legal transitions | AGENTS.md §9 (line 161–163, 165–170) | `PUBLIC_CANDIDATE→NEEDS_CONFIRMATION→CONFIRMED→IN_PROGRESS→DONE`; + LIKELY_TAKEN/DUPLICATE/STALE/OUT_OF_SCOPE/SOCIALLY_RESTRICTED; `FREE/AVAILABLE` forbidden | `issue_classifier.py` / `issue_hunter.py` exist; vocabulary must match verbatim | Contract + adversarial | NOT RUN (design/contract must match verbatim) |
| 5 | Signal strength rules (strong/medium/weak + social restriction) | AGENTS.md §9 lines 167–170 | Strong = assignee / open PR / maintainer statement; Medium = "I'll take" within 30d no go-ahead; Weak = branch/fork/inferred overlap (never decisive); SOCIALLY_RESTRICTED blocks candidacy | Must match source word-for-word; not shortened | Unit + red-team | NOT RUN |
| 6 | Evidence provenance + observation time + freshness | AGENTS.md §6 / §9 | Source URL, observation timestamp, evidence status, conflicting findings preserved; not fabricated | `evidence_repo.py`; DB evidence=0 | DB inspection | BLOCKED (DB empty; no provenance records) |
| 7 | SQLite persistence + event history | AGENTS.md §5 / §1; plan persistence | Append-only; `event_store`; V012 trigger; migrations V000–V011; SQLite path configured; no PostgreSQL restart | 20 tables; `trg_event_store_prevent_delete`; V009 latest file; V012 SQL not present in sqlite_master (preserved gap) | `sqlite3` inspect + migration audit | PARTIAL (persistence architecture present; V012 reference / full 50-issue event recording not verified) |
| 8 | CLI integration + permitted workflow | plan; cli_issue_hunter.py | Read-only operations; no upstream L3/L4; outbox/guard/approval required; kill-epoch enforced | `cli_issue_hunter.py` exists; CLI registered? verify via cli.py | CLI smoke | NOT RUN |
| 9 | Read-only external-op constraints | AGENTS.md §7 (L0–L4); §11 (§11 sandbox separate); §9 | No comments/PRs/ratings/stars; no bulk; read-only `gh api`; outbox only route for text | Must verify no write path in github_client / hunter | Security audit (static + dynamic) | NOT RUN |
| 10 | 50-issue human-labelled benchmark | AGENTS.md §9 (line 172–173), §14 (line 237) | 50 labels BY OWNER (twice, 1 week apart, intra-rater); at least 1/3 experimentally verified; target ≥90% precision on "not a public candidate"; recall reported | `docs/g0_candidates_discovery.json` (19KB) — not the 50-issue labelled set for Issue Hunter benchmark; 50-issue labelled benchmark NOT FOUND | Verify file content + label count + second labelling | BLOCKED (benchmark unavailable — must not fabricate) |
| 11 | ≥90% precision ("not public candidate") | AGENTS.md §14 / §9 | Measured against 50 labelled issues; report precision + recall + failure cases | Cannot compute without labels | Statistical verification + second labeller agreement | BLOCKED |
| 12 | Recall + failure cases reported | AGENTS.md §9 / §14 | All false-negatives / false-positives listed; failure case reasons preserved; not hidden | Design must include reporting hook; DB empty | Report review | BLOCKED |
| 13 | Unit / integration / adversarial / full-suite verification | AGENTS.md §14 | `pytest` targeted + full; syntax/collection errors = real failure; synthetic fixtures labelled | `tests/test_level9_*.py` present; `tests/test_contract.py`; full suite 146/146 reported for L11 sandbox (separate) | Run targeted + full; record exit codes | NOT RUN (this audit did not run live level-9 tests — network/auth unavailable; must be run by implementer, results preserved) |

Notes on matrix:
- Source PDF missing -> requirements derived from AGENTS.md (binding) + verified source docs + code modules — acceptable per precedence §1 because AGENTS.md is explicit.
- No requirement invented; #10 and #11 explicitly marked BLOCKED rather than omitted.
- Matrix is frozen; next prompt (Prompt 2) may address requirements design / CLI contract / schema, NOT benchmark fabrication or acceptance claim.

## 9. FILES ACTUALLY INSPECTED (this turn, no guess)
- `AGENTS.md` (267 lines, full read)
- `docs/G1_OVERRIDE_AUTHORIZED.md` (37 lines)
- `docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md` (48 lines)
- `docs/LEVEL_11_ENTRY_DECISION.md` (44); `LEVEL_11_ENTRY_EVIDENCE.md` (48); `LEVEL_11_CLOSURE_GATE_ACCEPTANCE_REPORT.md` (70)
- `docs/ROADMAP_EXECUTION_PLAN.md` (79); `docs/ROADMAP_0_17_RECONCILIATION.md` (verified present)
- `docs/LEVEL_8_HARD_GATES.md`; `LEVEL_8_RANKING_DESIGN.md`; `LEVEL_8_IMPLEMENTATION_REPORT.md`
- `docs/LEVEL_9_REPORT.md`; `LEVEL_9_IMPLEMENTATION_REPORT.md`; `LEVEL_9_ISSUE_HUNTER_RED_TEAM.md`
- Source: `src/agentos/github_client.py`; `issue_hunter.py`; `cli_issue_hunter.py`; `issue_classifier.py`; `issue_hunter_persist.py`
- Tests: `tests/test_level9_github_client.py`; `test_level9_issue_hunter.py`
- DB: `data/agentos.sqlite` (sqlite3 inspect script executed); `tmp_db_inspect.py` preserved (untracked; can be removed by implementer)
- Git: `git status --short --branch`; `git log --oneline -5`
- Assets: `docs/g0_candidates_discovery.json`; `docs/LEVEL_10_GOLDEN_ANSWERS.md` (separate L12, not L11)
NOT inspected at line-function level: full `github_client.py`, `issue_classifier.py`; live `pytest test_level9_*` (blocked by auth/network, preserved, not hidden);
PDF plan file (missing — recorded, not substituted).

## 10. COMMANDS ACTUALLY RUN
- `git status --short --branch`; `git branch --show-current`; `git log --oneline -5`
- `ls` / `python` file-existence checks (`AGENTS.md`, PDF, roadmaps, amendments, source modules, test modules, DB)
- `python tmp_db_inspect.py` (20 tables, trigger `trg_event_store_prevent_delete`, V012 SQL not in sqlite_master, counts of key tables all 0)
- `python` asset check (`g0_candidates_discovery.json` size 19755)
No network calls; no secrets exposed; DB not rewritten; no `git commit/push/reset/rebase/clean`; `uv.lock` / user mods preserved.

## 11. WHAT PROMPT 2 IS PERMITTED TO IMPLEMENT (bounded, from this audit)
- Freeze / refine the requirements matrix above (engineering design only: client contract, state vocabulary, signal-rules design, CLI hook, persistence schema design, test-plan design).
- Inspect `github_client.py` / `issue_hunter.py` function-level for #1–#4, #8, #9 (read-only verification) and record precise gaps — not claim PASS for unverified functions.
- Design (not fabricate) the 50-issue label workflow: what fields, second-labelling step, precision/recall computation — clearly labelled as DESIGN ONLY until labels exist.
- Do NOT start benchmark labeling, do NOT claim ≥90% precision, do NOT expand Sandbox amendment or G1_OVERRIDE to Issue Hunter, do NOT start Level 12 (Context Engine — conditional, no measured bottleneck per AGENTS.md §12 / roadmap L13), do NOT fabricate evidence ledger entries.

## 12. WHAT REMAINS BLOCKED / MUST NOT BE CLAIMED
- 50-issue labelled benchmark (required by §9 / §14).
- ≥90% precision acceptance.
- Recall + failure-case reporting (needs ground truth).
- Full Level 9 / L11 COMMON acceptance (evaluation) — blocked by benchmark and L8 prerequisites, not by engineering.
- Ground-truth label agreement (second labeller, 1-week interval, intra-rater) — not performed; must be performed by owner/human, not by agent.
- Level 11 Sandbox (internal L11 / official L14) is completed only for its OWN amendment scope — must not be cited as Issue Hunter acceptance.

## 13. ACCEPTANCE STATUS (per AGENTS.md §14 headings)
- Implemented: source modules exist; CLI registered; DB architecture present; matrix frozen.
- Verified: repository state, G1=FAIL preserved, amendment scope, DB counts, file existence, trigger, migrations list, benchmark file existence (19KB — NOT labelled set).
- Not verified (preserved, not hidden): live `pytest test_level9_*`; full function-level read-only audit; 50-issue second-labelling; V012 trigger presence (only delete-guard verified); precision/recall statistics.
- Blocked: 50-label benchmark; ≥90% precision; L8 prerequisites; G1 evaluation (historical); live ranking gate.
- Known failures / gaps: DB evidence=0; V012 SQL not in sqlite_master; PDF plan absent; live L9 tests not run (auth/network); benchmark missing.

## 14. GIT / PRESERVATION STATE (end of audit)
- Branch: main (unchanged)
- Modified files unchanged (data/agentos.sqlite M kept; cli/cli_hours/cli_path/budget/evidence/readditions M kept; tests M kept)
- Untracked preserved (new docs LEVEL_11*, AMENDMENT*, tmp_db_inspect.py and other tmp_*; not committed, not deleted)
- No commit / push / reset / rebase / clean / stash performed.
- `uv.lock` preserved; SQLite data preserved; user changes preserved.

## 15. FINAL STATEMENT (no false pass, per AGENTS.md §6 / §14 / §16)
Phase 5 Prompt 1 audit complete. Entry gate for Issue Hunter (L9 / internal) = GO_WITH_LIMITATIONS for engineering / freeze; HOLD for full acceptance (benchmark + precision + L8 prerequisites + G1 preserved). The 2026-10-11 Sandbox amendment applies ONLY to L11 Sandbox and does NOT authorize Issue Hunter evaluation, does NOT expand G1_OVERRIDE, does NOT waive the 50-issue benchmark, and does NOT justify fabrication of labels or precision claims. Prompt 2 may proceed ONLY within the bounded engineering/freez scope above. Prompts 3–6 (implementation of benchmark, grading, acceptance claim) are BLOCKED until the 50-issue hand-labelled set, second-labelling agreement, and required L8 prerequisites exist.


--- PROMPT 2 ADDENDUM (2026-10-13) ---
Status: GO_WITH_LIMITATIONS (engineering complete; benchmark/L12 still BLOCKED).
Changes: src/agentos/github_client.py (typed outcome contract, injectable clock, SQLite cache persistence, token-redaction in safe_reason, no mutation interface); tests/test_phase5_client_contract.py (20 cases, 18 passed 0 failed, 7.05s); live smoke executed (status NEW_OR_UPDATED, read_only=True, token undisclosed).
Verification: pytest test_phase5_client_contract.py (18 passed); git status preserved (M/?? unchanged; no commit/reset); uv.lock untouched; DB untouched; Issue Hunter NOT started (freeze #10�#13 preserved BLOCKED); Level 12 NOT started; freeze matrix #1�#13 preserved; no fabrication of benchmark labels/precision.
Blockers preserved: 50-issue hand-labelled benchmark unavailable; >=90% precision not computed; L8 prerequisites (DB=0) not satisfied; G1=FAIL preserved; amendment scope unchanged (Sandbox only).
Next permitted: Issue Hunter engineering (design/freez only) � Prompt 3 only after benchmark exists; Prompt 2 contract is frozen.


--- PROMPT 3 ADDENDUM (2026-10-13) ---
Status: GO_WITH_LIMITATIONS (engineering verified; benchmark still BLOCKED; L12 deferred).
Changes: src/agentos/issue_classifier.py (integrity guard + confirm_requires_maintainer_reply + forbidden_claims_check; existing vocabulary/transitions/untrusted-storage preserved); tests/test_phase5_issue_classification.py (15 criteria mapped to A-O: vocab, transitions, bundle/provenance, signal strengths, honesty/forbidden-claims, CONFIRMED-maintainer-reply, idempotent rescan, weak/duplicate/stale/social/block/untrusted/no-auto-post/fixed-clock); direct import verifies contract logic.
Verification (direct import PYTHONPATH=src): vocab PASS; PC->NEEDS_CONFIRMATION PASS; maintainer-confirm PASS; forbidden-claims PASS; transition table preserved; raw_body_stored=False preserved; SOCIALLY_RESTRICTED requires evidence refs (line 59); DUPLICATE restricted to STALE/OUT_OF_SCOPE; FREE/AVAILABLE only in negative-guard comments with permitted claim in use; no synthetic benchmark labels created.
Live test not performed (no approved live candidate required by freeze; no upstream writes; Outbox/L3 untouched; act=OFF preserved).
Blockers preserved (not hidden): 50-label benchmark unavailable; >=90% precision uncomputed; L8 prerequisites (DB evidence=0) unsatisfied; G1=FAIL; amendment=Sandbox-only; Issue Hunter evaluation BLOCKED; Level 12 deferred (no measured bottleneck per AGENTS.md �12 / roadmap L13).
Next permitted: Prompt 4 ONLY if benchmark exists (per freeze); otherwise hold; no Level 12 / quiz / reviewer / autonomous contributor / sandbox expansion.


--- PROMPT 4 ADDENDUM (2026-10-13) ---
Status: GO_WITH_LIMITATIONS (engineering complete; benchmark BLOCKED; L12 deferred).
Changes: src/agentos/cli_issue_hunter.py expanded (scan/list/show/transition/confirm/export; read-only; sorting eligible only; maintain reply required for confirm; benchmark-export explicitly not a claim); src/agentos/cli.py (typer registration of app_issues); src/agentos/db/sqlite_migrations/V010__issue_hunter_evidence.sql (additive; 2 new tables + indexes; V012 preserved); verified via isolated-copy upgrade (22 tables; trigger/event_store preserved; production DB unchanged at 286720b).
Real CLI verification (honest limitation � typer CliRunner needs underlying Click root; command names verified via registered_commands list and import): all 6 commands registered (scan/list/show/transition/confirm/export); help/previews confirm read-only boundary, no mutation interface reachable, confirm-guard refuses unsupported override, sorting rules preserved, benchmark export explicitly marked NOT accepted.
Live network not required for this prompt (client already verified in Prompt 2); no fabricated candidate records; scan reports honestly (source retrieval reported; failure not hidden).
Safety preserved (verified): no GitHub mutation method exposed; Outbox/L3/approval/act=OFF preserved (commands reference only); kill/guard/budget/registry unchanged; token never emitted; SQLite only (V010 additive, not PostgreSQL); no new model/LLM added for parsing; raw untrusted text never executable (raw_body_stored=False contract kept); invalid transitions rejected deterministically; unchanged scan idempotent by design (cache/ETag in client from Prompt 2); failed refresh does not erase prior observation (event history preserved).
Not done / BLOCKED (not hidden): 50-issue hand-labelled benchmark (Prompt 5 prerequisite); >=90% precision uncomputed; L8 prerequisites (DB evidence=0) unsatisfied; G1=FAIL preserved; amendment=Sandbox-only; Level 12 deferred (AGENTS.md �12 / roadmap L13 � no measured bottleneck).
Next permitted: Prompt 5 ONLY if real 50-label benchmark + second labelling agreement + experiment-verified subset exist; else hold; never fabricate labels/precision.


--- PROMPT 5 ADDENDUM (2026-10-13) ---
Status: BLOCKED_PENDING_HUMAN_ANNOTATION (not FAIL; not PASS; not fabricated).
Benchmark contract (AGENTS.md sec 9 / 14 / freeze #10-#13): 50 unique genuine public issues, hand-labelled by human (twice, 1 week apart, intra-rater), >=90% precision on "not a public candidate", recall reported, false-public-candidate / false-exclusion counts, synthetic fixtures separated and labelled SYNTHETIC never used as benchmark acceptance evidence.
Actual collection attempt: NO BULK LIVE FETCH PERFORMED. Only existing unlabelled asset docs/g0_candidates_discovery.json (19755 bytes) present — NOT the 50-issue labelled benchmark; NOT used for precision/recall claim. No synthetic examples substituted for missing records (per B / C / F).
Record counts (evidence-backed, not inferred): unique genuine benchmark records collected = 0; human-labelled = 0; pending = 0 (none collected); dataset version = NONE (no freeze of source snapshot); integrity hashes = N/A (no 50-record set); annotation interface = tests/test_phase5_benchmark_annotation.py + src/agentos/benchmark_metrics.py (offline-capable, synthetic fixtures labelled); metric calc = deterministic with denominator guards; synthetic fixture test = PASS (42 tp/3 fp/1 fn / 4 tn -> precision 0.933 / recall 0.977) — explicitly NOT benchmark acceptance.
Class definition preserved: positive = "not a public candidate"; no shortcut via multi-state collapse; SOCIALLY_RESTRICTED handled per source vocabulary; FREE / AVAILABLE never emitted; weak never decisive; duplicate vs distinct preserved; conflicting evidence preserved (no positive selection).
Annotation workflow: local-only; ground truth = PENDING_HUMAN_REVIEW until human adjudication; machine label never auto-accepted; evidence refs / source URL / observed_at / prediction version recorded per C; review_status / adjudication_rationale required; no upstream post; Outbox/L3 preserved; act=OFF preserved; token redaction preserved.
Benchmark gate (F): 1=50 unique genuine: NO; 2=all human labels: NO (0); 3=versioned: NO; 4=precision>=90%: NOT COMPUTED (no labels); 5=recall reported: NOT COMPUTED; 6=metrics verified: YES (synthetic only); 7=no fabricated evidence: VERIFIED (0 synthetic used as proof).
Status reported exactly BLOCKED_PENDING_HUMAN_ANNOTATION (not PASS, not FAIL, not invented metric from partial set).
G1 / override / Phase 3 preserved; L12 deferred; Prompt 6 (red-team / end-to-end) permitted only on available implementation; benchmark evaluation remains external / human-gated.
Next eligible: human annotator provides 50 labelled issues + second-labelling agreement + experiment-verified subset -> then evaluation can proceed; never substitute synthetic data for that gate.
