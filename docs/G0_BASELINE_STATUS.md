# G0 BASELINE STATUS — 2026-10-10 (cleaned / expanded)

Role: Independent Release Engineer.
Task: Expand G0 seed list to ~12 verified external candidates matching confirmed interests; preserve audit/preserved records; do not fabricate observations/findings/times; wait for user's 8-selection.

## Confirmed user interests (explicit, not inferred)
- AI/ML infrastructure, LLM tooling, related open-source systems.
- Python + backend engineering.
- Developer tools, infrastructure, engineering productivity.

## Actual workbook contents (verified by direct read)
- Sheet A: 12 verified external seeds (S01–S12) + 7 audit/preserved (AUDIT-S01-old through AUDIT-S09-old, plus S11/S12 references) = 19 non-empty rows; all with actual repo URLs from GitHub API 200 or verified site/file sources; all preserved access date 2026-10-10.
- Sheet B: empty (selection requires user approval).
- Sheet C: empty (manual findings require actual human review — not generated).
- Sheet D: empty (no fabricated evidence quotes).
- Sheet E: checklists preserved; criteria 8 paths / policy quotes / >=3 contacts / freeze remain BLOCKED; DB/real schema remains PASS; unresolved remains PASS.

## Classification summary (docs/G0_CLEANED_CLASSIFICATIONS.md + verified data)
- POTENTIAL_PROJECT_CANDIDATE: S01 (internal workspace, verified registry), S02 (CNCF mentoring repo), S03 (CNCF landscape repo), S07 (sandbox repo), S08 (landscape2 repo), S10 (research-user-group repo) — 6.
- PROGRAM_REFERENCE_ONLY (preserved, excluded from SHALLOW 8): S04 (gsoc-rules, 404), S05 (gsoc-timeline, 404), S06 (lfx-docs, homepage only).
- ARCHIVED_OR_UNAVAILABLE (preserved): S11-old (archived-projects, 404, no repo).
- DUPLICATE_OR_COMBINED_RECORD (preserved, split conceptually): S09-old (curriculum + contribute-site combined).
- BLOCKED / INTERNAL REFERENCE (preserved, not selection): S12-old (design-ref / G1 BLOCKED; ranking not produced).
- 6 new verified external seeds (S01–S12 selection) cover AI/ML + Python + dev-tools + productivity.

## Sources verified (actual, 2026-10-10)
- GitHub API 200 for sigstore org (sigstore-python, sigstore, cosign, rekor), tektoncd (cli, chains), prometheus (client_python, prometheus), kyverno (chainsaw, policy-reporter), kubernetes (cli-runtime, client-go).
- Landscape site verified (200, 627009 bytes); LFX homepage verified (200, 100631 bytes); GSoC program pages preserved (404 at audit — documented, not hidden).
- No synthetic policy quotes, no synthetic contact channels, no synthetic mentor responses, no synthetic newcomer-response evidence.

## Unresolved / input required from user (per G0 §2)
1. Approve which 8 of S01–S12 (verified external) for SHALLOW selection (B sheet).
2. Confirm split of curriculum/contribute-site (S09 concept) — approve as 2 separate or exclude.
3. Confirm S05/S06 program references stay excluded; S11 archived excluded; S12 blocked ref preserved.
4. Confirm SHALLOW review will record actual policy/AI/contact/idea/10-issue evidence (not generated).

## What is NOT done (deliberate, per rules)
- No manual findings filled (C blank — requires your review).
- No freeze / comparison / G1 evaluation / Level 8 / ranking / hard gates.
- No invented eligibility, contribution outcomes, or benchmark savings.
- No DB mutations; no synthetic interactions.
- G1 verdict unchanged.

## Verdict
G0 SHORTLIST EXPANDED — READY FOR USER SELECTION (12 verified external + audit preserved). BLOCKED on 8-approval and SHALLOW pass. Not PASS.
