PROMPT 2 READINESS — CONSOLIDATED OWNER INPUT REQUEST (2026-10-11)

Status: BLOCKED_ON_OWNER_INPUT (not READY_FOR_PROMPT_2).
Level 11: PARTIAL-ACCEPTED (amendment preserved; triggers NOT MET preserved; dependency-workflow evidence documented; full unconditional ACCEPTED blocked by unverified volume/digests — not hidden).
Proposal Evidence Auditor: NOT started (no module, no DB edit, per scope freeze).

WHAT ALREADY EXISTS (do NOT resupply) — verified this turn:
- docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md (L11-only waiver, NOT MET preserved)
- docs/LEVEL_11_CLOSURE_GATE_ACCEPTANCE_REPORT.md (PARTIAL-ACCEPTED, gap named)
- sandbox/stage_a/integrity_manifest.json (29 artifacts, registry pypi.org; integrity_path/is_complete=None — honest gap)
- sandbox/INTEGRITY_RESULT.md / stage_a/INTEGRITY_RESULT.md (uv.lock SHA e2bfe251... preserved; PASS)
- config/programs.yaml (timeline refs only; NO size/entry-cost)
- registry/orgs/open-os-demo.yaml (proposal_text=BLOCKED; proposal_estimate=ASSIST_ONLY)
- data/agentos.sqlite (evidence/interactions/projects/mentors/hours_log = 0; read-only preserved)
- docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md (critic-only freeze; depends on inputs)
- docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md (prior verification)
- sandbox/stage_a/dependency_workflow_completion_2026-10-11.md (this task's L11 evidence)

WHAT IS STILL MISSING — ask owner for exactly these, once each:

1. PROPOSAL DRAFT (source file / URL / pasted text). Confirm which project/idea it maps to (current registry points to open-os-demo with BLOCKED proposal_text — confirm if that is the intended target, or provide the real draft if different).

2. IDEA PAGE / PROJECT SOURCE. Confirm repository/path/URL for the idea the proposal addresses. Currently none found (scratch/ = sandbox only: stageb_live.py/test_prefetch.py/vol_hashes.txt; no idea/ page/ proposal-source file).

3. CHOSEN PROJECT SIZE + PROGRAM HOURS. programs.yaml has no size/entry-cost; DB hours_log = 0. Confirm: which size tier (the plan's size categories) applies, and provide entry-cost hours (or confirm whether to derive from existing logged work — currently none). If the project is open-os-demo, confirm size + milestone budget from config/budgets.yaml / config/prices.yaml if relevant.

4. EVIDENCE TO ADD (optional but needed for a meaningful critic): the ledger is genuinely empty (0 rows across evidence/projects/interactions/mentors/organizations). Ask: does the owner have evidence to import (interactions, mentor replies, PR references, eligibility checks), or should Prompt 2 begin with an empty-ledger diagnosis (the auditor's job per §6.10 / §13: identify unsupported claims and missing evidence — an empty ledger is a valid starting state if that is the owner's intent)? Do NOT invent mentor replies; a mentor reply is NOT a mandatory auditor input (plan §6.10 / §13; scope freeze line 3 — only draft + hours + ledger are prerequisites).

DO NOT invent: no substitute proposal, no synthetic idea page, no estimated hours without evidence, no fabricated ledger rows, no synthetic fixtures labeled real.

NOTE ON LEVEL 11 / AUDITOR SEPARATION: L11 dependency-workflow evidence is now documented; do not conflate with Prompt 2 readiness — Prompt 2 is gated by input sources, not by L11 status. Do not start auditor source edits until sources 1-3 (and 4 if needed) are confirmed.
