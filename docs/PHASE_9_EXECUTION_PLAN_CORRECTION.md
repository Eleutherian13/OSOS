# PHASE 9 CANONICAL EXECUTION-PLAN CORRECTIONS (2026-10-14) — reflects user's 6 points; does NOT restart P1

SOURCE OF CONFLICT RESOLVED: user's 6 corrections + v2.1 §4 (CORE/NEXT/DEFERRED) + AGENTS.md §15 (current-state snapshot not verified automatically) + PHASE_8_FINAL_ACCEPTANCE.md.

CORRECTIONS APPLIED (each mapped to evidence; none hidden):
1. L2-3: empty DB handled separately from implementation verification (test_level2_3_integration.py verified; db_counts.py / DB=evidence=0 preserved). Real-data acceptance remains BLOCKED until real paths/evidence provided — not fabricated.
2. L8/L9 vs G1: G1=FAIL preserved in both doc copies; root copy absence documented; G1_OVERRIDE_AUTHORIZED permits development but does NOT pass G1; L8 ranking and P3 integrated verification preserved independently.
3. L11: 50-issue benchmark BLOCKED (labels missing); 13/13 tests preserved for implementation only; Sandbox Stage B evidence NOT substituted for Issue Hunter correctness; AMENDMENT doc applies to entry trigger only.
4. L12: syntax/test-collection verified (current tests load; fix_syntax.py applied earlier); golden-answer evaluation BLOCKED until genuine second owner session + ≥7-day separation + confirmation; no simulated time/owner.
5. L14: existing Sandbox artifacts (sandbox/, LEVEL_11_SANDBOX_*, test_level11_sandbox_orchestrator.py) preserved; full official L14 acceptance NOT pursued; act=OFF; trigger/amendment unresolved.
6. L16: Design A (auditor_service + validation/contract tests + doc) PASS at scoped implementation; real E2E BLOCKED (DB=0; inputs missing); Design B deferred (auth/dataset/method); neither blocks P9 CORE/regression/security.

IMPACT ON PHASE ORDER: P9 (this phase) proceeds with verification/hardening; P1-P8 conclusions not restarted; deferred items (L13, L14 full, L15, Policy, Design B) remain deferred with triggers listed.

NOT CHANGED BY THIS DOC: production DB; G1 records; P8 artifacts; uv.lock; Guard/Outbox/budget/kill; upstream posture (act=OFF).
