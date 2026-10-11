# CLEANED SEED CLASSIFICATIONS — 2026-10-10

Audit of all 12 rows (workbook A_Seed_Candidates, rows 4-15, verified by direct read):

| ID | Classification | Evidence / Reason | Action |
|---|---|---|---|
| S01 | POTENTIAL_PROJECT_CANDIDATE | Workspace registry file (verified); real repo; real path. Internal to this project — acceptable as a candidate only if user's interest includes this org. | Keep; clarify if user's interest is this workspace or external OSS. |
| S02 | POTENTIAL_PROJECT_CANDIDATE | CNCF mentoring repo verified (GitHub API 200); real external contribution path. Page /mentoring/ returned 404 — documented, not hidden; repo-level evidence sufficient for seed. | Keep. |
| S03 | POTENTIAL_PROJECT_CANDIDATE | Landscape repo verified; site verified (200, 627009 bytes). Real external project. | Keep. |
| S04 | PROGRAM_REFERENCE_ONLY | Config URL verified; page 404; no repo; no project-level evidence. Not a contribution path. | Do NOT count as SHALLOW candidate; keep as program-ref only. |
| S05 | PROGRAM_REFERENCE_ONLY | Config URL verified; page 404; no repo; no project-level evidence. | Same — reference only. |
| S06 | PROGRAM_REFERENCE_ONLY | LFX homepage 200; docs subpath unverified; no repo/project. | Reference only. |
| S07 | POTENTIAL_PROJECT_CANDIDATE | Sandbox repo verified; site /sandbox-projects/ 404 (preserved). Real repo = contribution path possible. | Keep (with caveat). |
| S08 | POTENTIAL_PROJECT_CANDIDATE | Landscape2 repo verified; landscape site verified. Real external tooling. | Keep. |
| S09 | DUPLICATE_OR_COMBINED_RECORD | Two repos (curriculum + contribute-site) in one row; neither individually selected. Should be split OR kept as option set, not a single candidate. | Split or ask user which; do not treat as one SHALLOW path. |
| S10 | POTENTIAL_PROJECT_CANDIDATE | Research-user-group repo verified (core, not fork). Real external group. | Keep (with caveat). |
| S11 | ARCHIVED_OR_UNAVAILABLE | /archived-projects/ 404; no repo; reference only. Not live contribution path. | Remove from SHALLOW list; may keep as archived ref. |
| S12 | INTERNAL_PROJECT_REFERENCE | References design contract for ranking (not produced); not a contribution path. Blocked by G1. | Remove from SHALLOW; keep as documentation boundary only. |

Cleaned count of real external contribution candidates (excluding references/duplicates/archived/internal): S02, S03, S07, S08, S10 = 5 real. Plus S01 (internal) if user's interest covers it = 6. S09 split could add 1-2 = 7-8. To reach 8 real SHALLOW paths, need user to either (a) confirm S01 + split S09 + approve S07 + approve S10, or (b) provide additional interest tags for other CNCF/GSoC/LFX projects (e.g., Cilium, Kubernetes SIG, etc.).

Requested user input (per G0 §2 — no silent inference):
1. Interest area: CNCF / GSoC / LFX / internal workspace / mix?
2. Which of S02/S03/S07/S08/S10 (+ S01 if included) to approve for 8-selection?
3. Should S09 be split (curriculum vs contribute-site) — approve one or both?
4. Should S04/S05/S06 (references) stay in workbook only, excluded from 8?
5. Should S11 (archived) and S12 (design-ref) be removed from A or kept with clear non-candidate status?
