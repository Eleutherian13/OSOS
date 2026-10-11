# PROPOSAL EVIDENCE AUDITOR — SCOPE FREEZE (2026-10-11)
SELECTED: Proposal Evidence Auditor (§13, conditional — only with inputs)
TRIGGER: not met until owner provides proposal draft + hours + mentor reply
INPUTS STATE: proposal draft MISSING; entry-cost hours MISSING; mentor reply MISSING
ACCEPTANCE (critic-only, never rewrites proposal):
  - For any provided proposal input: list unsupported claims (need source quote+timestamp), uncovered deliverables (vs evidence ledger), unvalidated assumptions, likely mentor challenges.
  - NEVER produce replacement proposal prose (§13 explicit: critic-only, never rewrites proposal).
  - Preserve G1=FAIL, G1_OVERRIDE_AUTHORIZED, SQLite, uv.lock, user mods, act=OFF, Guard/Outbox.
DEPENDENCIES: evidence ledger (exists: LEVEL_8_EVIDENCE_LEDGER_AUDIT.md); registry (exists); proposal draft (BLOCKED — owner must provide).
OUT-OF-SCOPE: proposal drafting, policy extraction, L12 context engine, PR shepherd, capacity planner, sandbox extension.
TESTS: none invented; if inputs arrive, run critic-check against inputs; if no inputs, state BLOCKED.
