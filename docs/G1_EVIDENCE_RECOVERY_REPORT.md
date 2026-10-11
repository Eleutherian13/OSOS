# G1 EVIDENCE RECOVERY REPORT — 2026-10-09

Task: Evidence-recovery audit only (no ranking / gates / Level 8 implemented; G1 verdict unchanged).
Status of source records: NOT RECOVERED.

## Verdict
G1 BLOCKED — REQUIRED RECORDS NOT FOUND.

Reason: The original eight-candidate manual/tool comparison requires three missing artifacts that were never produced or preserved in this workspace: (a) the eight-candidate identity list and manual findings, (b) the tool-assisted findings for those same eight, (c) recorded manual/tool elapsed working times (including human review time). Without all three, neither material-discovery (criterion A) nor time-saving (criterion B) can be evaluated. No substitution permitted by the audit rules.

## Locations searched (actual, no omission claimed)
- docs/ (BUILD_STATE.md, G1_GATE_REPORT.md, LEVEL_0–7 reports, contracts, LLM_RUNTIME_CONTRACT.md) — no candidate list, no spreadsheet, no manual/tool comparison.
- evals/ — .gitkeep only (empty).
- registry/orgs/ — open-os-demo.yaml (project registry, not candidates / not 8 records).
- tests/ / migrations/ / src/ — schema and code only; no fixture dataset of 8 candidates; no ranking module (expected — Level 8 not authorized); no spreadsheet exports.
- Root — no .csv/.xlsx/.ods/.tsv; contracts and prompts only.
- Git history (git log --oneline -- docs/ registry/): single commit (4a1ac61 first commit); no deleted spreadsheet recovered; git branch -a shows no alternate branch with baseline.
- DB (localhost:5432): unreachable (timeout at 13:13); no running instance with candidate evidence table; migrations V001–V009 contain no candidate-tracking table.

## Records found
- docs/G1_GATE_REPORT.md (existing, unmodified): documents previous BLOCKED decision; contains the G1 threshold definition (A or B); does not contain the 8-candidate dataset or measurements.
- docs/LEVEL_7_REPORT.md (created earlier in session): Level 7 verified; explicitly does not claim G1 pass; does not contain benchmark data.
- docs/BUILD_STATE.md: LEVEL 7 ACCEPTED / G1 BLOCKED preserved independently; no benchmark data.
- No spreadsheet, no CSV, no exported evaluation record, no dated tool-output log for the 8-candidate set found anywhere in the workspace.

## Original baseline (recovered?)
NOT RECOVERED.
- The eight candidates: unknown.
- Manual findings: unknown.
- Tool findings: unknown.
- Source links / policy evidence per candidate: unknown.
- Manual time spent: unknown (no recorded measurement found; cannot reconstruct without inventing).
- Tool execution / human review time: unknown.
- Evidence needed to identify a material discovery missed by either process: unavailable.

## Evidence supporting material discovery (criterion A)
NONE AVAILABLE.
No source link, no policy-change record, no hidden-contact-rule evidence, no stale/blocked-assumption evidence tied to any of the eight candidates is present. Nothing to compare between manual and tool outputs.

## Evidence supporting time saving (criterion B, >=2 hours, same 8 candidates + human review)
NONE AVAILABLE.
No manual elapsed working time recorded; no tool-assisted elapsed working time recorded; no human-review-time record for tool output; no fixed-clock test record. Cannot compute delta; no fabricated comparison permitted.

## Missing records (explicit, not hidden)
1. 8-candidate identity list.
2. Manual baseline findings (with source links / policy evidence).
3. Tool-assisted findings for the same 8 (with evidence provenance).
4. Actual manual working-time measurement.
5. Actual tool-assisted working-time measurement (execution + human review).
6. Evidence needed to identify at least one material fact missed by one process.

## Can the benchmark be evaluated reliably?
NO. The required dataset is missing entirely, not partially. Partial recovery is insufficient because both criteria A and B require comparing the same eight candidates across both processes. Reconstruction from code components (readiness.py, model_wrapper, registry) is explicitly disallowed: the audit rules forbid inferring missing evidence from the existence of a component.

## What was NOT done (per audit rules)
- No ranking / hard-gate / Level 8 implementation.
- No new candidates substituted.
- No web research / external fetch to invent baseline.
- No reconstructed / estimated timings presented as historical facts.
- No modification to docs/G1_GATE_REPORT.md (verdict unchanged at BLOCKED).
- No claim of material discovery or time saving made without source.

## References (actual files inspected during recovery)
docs/G1_GATE_REPORT.md (unmodified); docs/BUILD_STATE.md; docs/LEVEL_7_REPORT.md; registry/orgs/open-os-demo.yaml; git log (4a1ac61); migrations/V001–V009; tests/test_level7_*.py; src/agentos/readiness.py (not used as evidence substitute).

## Verdict (single, required format)
G1 BLOCKED — REQUIRED RECORDS NOT FOUND.
