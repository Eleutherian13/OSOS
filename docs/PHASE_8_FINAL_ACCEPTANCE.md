# PHASE 8 FINAL ACCEPTANCE — PROPOSAL EVIDENCE AUDITOR / LEVEL 16 / DESIGN A (2026-10-14)

Controlling sources: AGENTS.md §4/§14/§6; original v2.1 plan §13; docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md; docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md; docs/G1_OVERRIDE_AUTHORIZED.md; docs/P7_FINAL_ACCEPTANCE.md; docs/P7_CROSS_CUTTING_SECURITY_REPORT.md; docs/PHASE_8_BASELINE_2026-10-14.md.

Additive only. References prior artifacts; no duplication of full detail.

## 1. Scope (corrected)

Design A (deterministic / critic-only) preserved; Design B deferred (authorization + dataset + validated-method not granted; no source artifacts); Level 16 conditional (§13); no Level 13/14/15 expansion; G1=FAIL preserved (docs/G1_OVERRIDE_AUTHORIZED.md = NOT PASS; root copy NOT PRESENT — contradiction resolved); Level 11 benchmark BLOCKED (separate); Level 12 syntax/test collection preserved (separate); empty DB at L2–3 does not prove missing implementation.

## 2. Changes made (verified)

- `src/agentos/core/auditor_service.py`: idea/hours file open + URL-marker (no invention), provenance dict, evidence_gap (actual DB count preserved), source_map_ok requires all three inputs.
- `tests/test_auditor_input_validation.py` (new, SYNTHETIC, 8 pass): all-present, missing-proposal, empty-proposal, URL-mismatch, missing-hours, zero-DB, malicious-text, provenance.
- `tests/test_auditor_output_contract.py` (new, SYNTHETIC, 9 pass): permitted categories, mentor-block, mentor-allowed, no-rewrite, adversarial-quoted, secrets, UNKNOWN, mandatory-gap, bounded-ref.
- `docs/PHASE_8_BASELINE_2026-10-14.md`: P8-1 baseline (paths, corrections, prerequisites).

No edits to: `docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md` (already correct); `docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_...`; `cli_auditor.py` (already critic-only); `auditor_finding.py` (already strict); production DB; G1; `uv.lock`; Guard/Outbox/kill/budget.

## 3. Requirement-to-code-to-test-to-result (summary)

| Requirement | Evidence | Status |
|---|---|---|
| Design A scope preserved | module + scope doc + CLI docstring | PASS |
| Design B deferred (auth/dataset/method) | no artifacts; conditions listed | DEFERRED |
| Proposal input validation | service edit + 8 synthetic tests | PASS |
| Idea URL/content | service reads file / marks URL unretrieved | PASS |
| Hours log | service reads / reports missing | PASS |
| Evidence linkage (DB SELECT) | `_db_counts()` preserved; gap labeled | PASS |
| Provenance fields | `load_input_ids` provenance + schema `EvidenceLink` | PASS |
| Missing ≠ FALSE; UNKNOWN preserved | schema + tests 07/08 | PASS |
| Owner labels required | BLOCKED (not provided; no fabrication) | BLOCKED |
| Critic-only / 4 categories | CLI + schema + tests 01/02/03 | PASS |
| No proposal rewrite | test 04 + module inspection + literal "pass" | PASS |
| No fabricated mentor/reviewer/label/time | test 02/03 + schema validator | PASS |
| Injection (adversarial quoted, not executed) | test 05 + P7 adapter isolation | PASS |
| Secret hygiene | test 06 + edit audit (no secrets) | PASS |
| People-data (public role; no inference) | design preserved; no new inference | PASS |
| Read-only DB / 0 upstream | `sqlite3` SELECT; git status shows only artifacts | PASS |
| Real-data gate | prerequisites listed; DB `evidence=0` preserved | BLOCKED |
| G1/F/P7/SQLite/V012/uv.lock/act=OFF | verified; 1 new doc + 2 test files only | PASS |

## 4. Implementation verification: PASS

Code verified (service edit + domain schema + CLI contract); 17/17 synthetic tests pass; no failures misreported; fixtures clearly labelled SYNTHETIC; test results match current code; DB unchanged.

## 5. Real-data E2E: BLOCKED (explicit, not hidden)

Mandatory prerequisites missing (verified by direct inspection + `load_input_ids` + DB query, not assumed):
- Proposal draft file/content: MISSING (registry `proposal_text=BLOCKED`; no file in docs/src/scratch).
- Idea-page URL/content: MISSING (no source file; URL not verified from authorized retrieval path).
- Programme-hours log / entry-cost: MISSING (DB `hours_log=0`; `config/programs.yaml` has timelines not size estimates).
- Evidence-ledger references linked to proposal claims: MISSING (`DB:evidence=0` preserved; no links).
- Owner labels (if evaluation demands): NOT PROVIDED.
- Source-map confirmation (proposal→idea→project): UNVERIFIED (scope freeze requires owner confirmation).

Status not fabricated to PASS. Evidence gap preserved as `DB evidence count = 0`. Real-data evaluation does not run against synthetic fixtures.

## 6. Design B: DEFERRED

Conditions (from scope freeze + AGENTS.md §4): separate owner authorization; appropriate dataset; validated analysis method; provider/integration if needed. None met; no artifacts created or altered.

## 7. Security / preservation verification

- Production data read-only (`sqlite3.connect` SELECT; no `INSERT/UPDATE/DELETE`).
- Production count preserved (`evidence=0`; not rewritten).
- No secret in edit or findings (`proposal_rewrite_check`, source refs, explanation contain no credentials).
- No upstream / no external request / `act=OFF`.
- Guard/Outbox/approval/kill/caps/budgets untouched (P7 accepted at design/test; live endpoint/model limitations preserved separately).
- Git: only audited `auditor_service.py` edit + 2 new test files + 2 docs; 0 commits / pushes / resets / cleans.
- Both G1 records preserved (docs copy present; root copy NOT PRESENT — documented); `G1=FAIL` unchanged.

## 8. Outstanding limitations (explicit, not hidden)

- Real proposal / idea / hours / evidence / labels: owner must provide.
- Level 11 50-issue benchmark: BLOCKED (separate from L16; not addressed here).
- Level 12 syntax/test-collection: preserved (separate; `tests/test_auditor_domain.py` exists, no false claim made).
- Design B: deferred by authorization, not by code failure.
- No live-source fetch / external-license audit performed (P7-E live audit BLOCKED, as previously documented — not substituted).

## 9. Final disposition

**Phase 8 (Proposal Evidence Auditor, Level 16, Design A):** Implementation verified (`PASS`); real-data E2E `BLOCKED` (prerequisites listed); Design B `DEFERRED`; preservation `PASS`; security `PASS`; no new official level started; no upstream action; no fabricated evidence, label, mentor reply, or benchmark result.
