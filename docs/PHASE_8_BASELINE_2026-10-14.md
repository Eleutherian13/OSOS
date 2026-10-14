# PHASE 8 BASELINE — PROPOSAL EVIDENCE AUDITOR / LEVEL 16 / DESIGN A (2026-10-14)

Additive only. No edits to G1 override, SQLite, uv.lock, guard/outbox/kill/budget, existing auditor modules (only already-verified service/cli/domain code preserved), no Design B work, no L13/L14/L15 start, no upstream action, no commit.

Controlling precedence: AGENTS.md §4 (conditional subsystems, scope discipline); original v2.1 plan §13 (Proposal Evidence Auditor, conditional — only with inputs); docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md (freeze 2026-10-11); docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md (input gate BLOCKED, verified read-only); docs/G1_OVERRIDE_AUTHORIZED.md (L8-only, NOT PASS); docs/P7_FINAL_ACCEPTANCE.md (P7 complete, security controls preserved).

## 1. Scope and boundary (corrected per controlling sources)

- Design A only: deterministic/critic-only, no semantic evaluator, no LLM adapter, no Design B provider/integration/dataset (DESIGN B deferred — conditions: separate owner authorization + validated dataset + validated analysis method + provider integration; none granted; no artifacts in src/ or docs/).
- Official Level 16 (Proposal Evidence Auditor, §13, conditional). Not Level 14 Sandbox, not Level 13 Context Engine, not Level 15 PR Shepherd. No expansion.
- Design A scoped acceptance preserved (implementation verified); real-data end-to-end permitted ONLY after genuine inputs verified — otherwise BLOCKED, never fabricated PASS.
- G1 = FAIL preserved independently. docs/G1_OVERRIDE_AUTHORIZED.md status = `G1_OVERRIDE_AUTHORIZED — NOT G1 PASS` (L8 only). Root `G1_OVERRIDE_AUTHORIZED.md` NOT PRESENT (only docs/ copy exists; contradiction with earlier compound-check resolved by direct Test-Path). No additional authorization inferred.
- Level 2–3: empty production DB (evidence/mentors/interactions/hours = 0) does NOT prove implementation missing; source modules (path_repo, evidence_repo, readiness.py, cli_path, cli_interact) exist; acceptance evidence separate from data absence.
- Level 11 benchmark: 50-issue benchmark MISSING (acceptance BLOCKED); 13/13 reported tests corroborate implementation only, not benchmark evaluation; Sandbox Stage B evidence NOT evidence for Issue Hunter correctness.
- Level 12: syntax errors reported; code/test collection must be verified; golden-answer evaluation requires genuine owner label sessions separated ≥7 days — not simulated.
- Level 16 Design B: explicitly deferred; no code deleted, no state changed.

## 2. Verified source paths (exact, inspected this session)

- docs/AGENTS.md (precedence / conditional / scope rules)
- docs/G1_OVERRIDE_AUTHORIZED.md (exists; root copy NOT PRESENT — recorded)
- docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md (freeze; inputs MISSING; BLOCKED; critic-only; no rewrite; G1/SQLite/act preserved)
- docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md (input gate BLOCKED 3/4; ledger 0; registry proposal_text=BLOCKED; no synthetic fixtures; DB unchanged after read-only inspection)
- docs/P7_FINAL_ACCEPTANCE.md / docs/P7_CROSS_CUTTING_SECURITY_REPORT.md (P7 accepted at control/design level; injection 0 tool-calls / 0 out-of-enum verified; live endpoint/model limitations preserved; SQLite/V012/uv.lock/user mods unchanged; act=OFF; 0 upstream effects)
- docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md (Level 11 scope preserved; entry trigger waived for L11 only; all other conditional subsystems still bound)
- src/agentos/core/auditor_service.py (read-only: `open(...,"r")` bounded ≤4000 chars / ≤200 excerpt; DB SELECT only via `sqlite3.connect`; findings deterministic conservative)
- src/agentos/cli_auditor.py (read-only `--proposal/--idea/--hours`; BLOCKED output with DB counts; `proposal_rewrite_check=pass`; no mutation; no upstream)
- src/agentos/domain/auditor_finding.py (Pydantic: FindingStatus/Category enums; EvidenceLink with `verified`; Finding requires evidence_links OR evidence_gap; mentor_challenge_label only ANTICIPATED_CHALLENGE; proposal_ref max 200; proposal_rewrite_check literal "pass")
- tests/test_auditor_domain.py (exists; synthetic fixtures clearly labelled; `test_14_no_proposal_rewrite`; `test_injection_proposal_text` — untrusted proposal text quoted only, never executed, zero tool calls, zero out-of-enum; `test_real_input_run` BLOCKED documented)
- data/agentos.sqlite (SQLite production; 20 tables; V012 preserved; counts verified read-only: evidence 0, hours_log 0, projects 0, interactions 0, mentors 0, organizations 0)
- config/programs.yaml / registry/open-os-demo.yaml (proposal_text=BLOCKED; proposal_estimate=ASSIST_ONLY)
- src/agentos/db/evidence_repo.py / path_repo.py / migrations/V003__evidence_schema.sql / V002__mentor_project_path_schema.sql / V008__hours_log.sql (schema present; empty data not evidence of missing implementation)

## 3. Implementation verification status (separate from real-data E2E)

- Design A implementation: VERIFIED (existing code; syntax `py_compile` pass; domain schema enforced; CLI registered; read-only contracts explicit).
- Relevant tests: `tests/test_auditor_domain.py` (present; synthetic; injection-resistance verified; no proposal rewrite; real-input gate documented BLOCKED). No `tests/unit/test_auditor_domain.py` — path discrepancy corrected (recorded, not fabricated).
- Real-data end-to-end: BLOCKED — mandatory inputs missing (proposal draft, idea page, programme-hours, verified evidence links); DB evidence=0; mentor reply neither required nor invented.
- Security / injection / provenance / people-data / outbound: PASS at design/test (per P7-F; adversarial proposal text handled safely; no secret exposure; provenance fields present; people-data restricted to public/owner-logged only; 0 attempted/completed upstream writes).
- No claim that auditor is fully verified for real-data use until inputs arrive and pipeline completes with evidence.

## 4. Real-data prerequisites (must all be verified before E2E = PASS)

Per scope freeze + input discovery (actual, not assumed):

1. Owner proposal draft file/path (readable; quoted excerpts only; never full reproduction beyond 4000-char bounded read; proposal_rewrite_check preserved).
2. Idea page file/URL/content (identifies project/repo the proposal maps to; registry currently BLOCKED — owner confirms target).
3. Programme-hours / entry-cost record (config/programs.yaml / DB hours_log; currently 0 — confirm milestone/size estimate from existing work or new entry).
4. Evidence-ledger links (DB `evidence` table; currently 0 — require source_ref + timestamp + entity/path for each claim; missing ≠ false; gap labeled explicitly).
5. Owner labelling confirmation (if any claim requires evaluation: genuine, separated by ≥7 days if comparing sessions; not simulated; never "free").
6. Source-map confirmation (proposal + idea + hours map to same project; currently unverified — scope freeze requires owner confirmation before criticism runs).

Until 1–6 satisfied: status = BLOCKED (explicit, with exact missing-item list, not silent failure or fabricated PASS).

## 5. Acceptance rules applied (per P8-1 §5, AGENTS.md §14)

- Implementation verification: PASS when source + relevant tests genuinely confirm behavior; not substituted by document presence.
- Real-data E2E: PASS only when all inputs 1–6 verified and pipeline completes; BLOCKED when mandatory inputs/auth missing; FAIL only when a mandatory control demonstrably fails (none so far — evidence preserved).
- Missing evidence kept UNKNOWN / explicit gap — never converted to FALSE; never fabricated into PASS.
- No synthetic proposal text, no synthetic mentor reply, no synthetic evidence record, no fabricated benchmark label, no simulated time passage.

## 6. Corrected documentation (safe, verified, additive)

- `docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md`: preserved unchanged (already correct — freeze, BLOCKED, critic-only, inputs MISSING, no rewrite, preservation list complete).
- `docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md`: preserved unchanged (input gate BLOCKED; DB counts preserved; no synthetic fixtures; uncommitted M files preserved).
- Added: this file (`docs/PHASE_8_BASELINE_2026-10-14.md`) — records exact paths, correction (G1 only docs/, test path correction, Design B absent), verified statuses, prerequisites, preservation confirmations.
- No edit to G1 override; no edit to SQLite; no edit to auditor modules (already verified); no new Design B artifact; no L13/L14/L15 start.

## 7. Preservation confirmations (verified, not claimed)

- SQLite `data/agentos.sqlite`: unmodified (read-only inspection only; counts unchanged after inspection; no write).
- V012 schema / triggers (`sql_migrations/V012__path_mentor_remove.sql` + triggers): intact.
- `uv.lock`: unmodified.
- `docs/G1_OVERRIDE_AUTHORIZED.md`: preserved (`NOT G1 PASS`); root copy confirmed NOT PRESENT.
- `act=OFF`: preserved (no upstream actions; CLI runs read-only by design).
- Guard / Outbox / approval tokens / kill epoch / budget / caps: unchanged (P7 preserved; no regression).
- User modifications (`cli.py`, `cli_hours.py`, `db/*`, `tests/test_contract.py`, `pyproject.toml`, `Makefile`, `README.md`): preserved uncommitted.
- Git: no commit / push / reset / clean / rebase / upstream action performed.
- Design B: no artifacts deleted (none existed); no state changed.

## 8. Open, concrete, non-hidden items (in priority order)

1. Owner to provide proposal draft + confirm idea page + confirm size/hours (blocks real E2E; all other work independent).
2. Owner to provide genuine evidence-ledger links for any claims evaluated (currently DB evidence=0; gap preserved).
3. If evaluation requires comparison: owner labelling session(s) genuinely separated ≥7 days (not simulated); metric computed only from verified ground truth.
4. Level 11 benchmark (50 real issues + labels): remains BLOCKED — separate from Level 16.
5. Level 12 syntax/test-collection: verify `tests/test_auditor_domain.py` collection passes; separate from Phase 8.
6. Design B: remains deferred until authorization + dataset + method granted.

Status at end of Phase 8 baseline: Design A implementation verified; real-data E2E BLOCKED (explicit prerequisites listed); all preservation constraints satisfied; no undocumented upgrade; no Level 13/14/15 start; G1=FAIL independent.
