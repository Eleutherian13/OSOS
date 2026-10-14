# PHASE 9 — PRODUCTION HARDENING — ENTRY CHECKLIST (NOT STARTED)

Status: **ENTRY CHECKLIST ONLY — NO IMPLEMENTATION BEGINNED.** Per user's instruction: "Prepare the entry checklist for Phase 9 production hardening, and do not begin Phase 9 implementation until its scope and prerequisites are verified."

This document is the prerequisite gate, not authorization to start.

## Controlling scope (from plan / AGENTS.md / P8 final)

- Phase 9 = official Level 17 (production hardening / final acceptance) per original v2.1 plan and P8-1 phased order.
- Conditional / deferred work (Level 13 Context Engine, Level 14 Sandbox, Level 15 PR Shepherd, Policy LLM extractor, Design B Level 16 deferred) remains tracked, NOT started by Phase 9.
- Phase 8 (Design A Proposal Evidence Auditor / Level 16) is completed and preserved; this checklist references it, does not redo it.

## Prerequisites to verify BEFORE any Phase 9 implementation

1. **Phase 8 closure confirmed (this session)** — verified: `docs/PHASE_8_FINAL_ACCEPTANCE.md` present (6372 bytes); 17/17 synthetic tests pass; real-data E2E BLOCKED (documented); Design B DEFERRED; preservation verified.
2. **Real-data E2E prerequisite resolved OR acknowledged** — proposal/idea/hours/evidence/owner-labels remain missing; Phase 9 must not fabricate inputs to clear this.
3. **G1 status preserved** — `docs/G1_OVERRIDE_AUTHORIZED.md` intact (`NOT G1 PASS`); root copy confirmed not present.
4. **P7 acceptance preserved** — `docs/P7_FINAL_ACCEPTANCE.md` / cross-cutting security preserved; SQLite/V012/uv.lock unchanged; `act=OFF`; 0 upstream.
5. **Design B authorization / dataset / method / provider** — still deferred; Phase 9 must NOT expand into Design B.
6. **Level 11 benchmark** — 50-issue benchmark still BLOCKED (separate; not P9's job to fabricate labels).
7. **Level 12 syntax/test-collection** — preserved; any fixes must be evidence-backed and separate from P9.
8. **Sandbox / Level 14 trigger** — not met; amendment (11-11) only waived entry trigger for Level 11, not Level 14; Phase 9 does not expand Sandbox.
9. **Scope / budget / freeze** — confirm with controlling sources (AGENTS.md §4/§6/§14; original plan) that Phase 9 scope (migration/recovery/regression/static/config/logging/full-suite) is still authorized and not over-expanded.
10. **User / owner authorization for Phase 9 start** — required, since P8 ended with BLOCKED real-data gate and unresolved prerequisites.

## Required verification before first Phase 9 edit

- [ ] Confirm above 10 prerequisites against current repo state (re-run `git status`, DB counts, G1 file check, test counts).
- [ ] Confirm scope from `docs/ROADMAP_EXECUTION_PLAN.md` / `AGENTS.md` §4 (CORE vs NEXT vs DEFERRED) — Phase 9 should stay within production-hardening (migration/recovery/regression/static/config/logging/safety-suite), not pull in deferred subsystems.
- [ ] Confirm no hidden dependency on Phase 8's missing real inputs (Phase 9 must work with current verified baseline, not wait for proposal draft).
- [ ] Confirm preservation rules still bind: SQLite, `uv.lock`, G1, `act=OFF`, Guard, Outbox, kill/caps/budget.
- [ ] Confirm exit rule: Phase 9 stops at its own final report; does not restart P1–P7 or invent P10.

## Blockers that must be resolved or explicitly deferred (not hidden)

- Real proposal/idea/hours/evidence (P8): BLOCKED — Phase 9 must not manufacture substitutes.
- Level 11 benchmark labels: BLOCKED — separate; Phase 9 must not fabricate.
- Design B authorization/dataset: DEFERRED — Phase 9 must not start Design B.
- Level 13/14/15 triggers: CONDITIONAL — Phase 9 only if prerequisite bottleneck is verified.

## What is NOT in Phase 9 (preserved)

- No proposal rewriting / no prototype drafting for missing proposal.
- No synthetic evidence inserted into DB to clear P8 gap.
- No Design B provider integration.
- No new upstream message / PR / comment.
- No alteration to P8 artifacts (`PHASE_8_FINAL_ACCEPTANCE.md`, `PHASE_8_BASELINE_...`, test files, `auditor_service.py` edit from P8-2).

## Evidence artifacts referenced by this checklist

- `docs/PHASE_8_FINAL_ACCEPTANCE.md` — Phase 8 closure (final status).
- `docs/PHASE_8_BASELINE_2026-10-14.md` — Phase 8 scope / prerequisites.
- `tests/test_auditor_input_validation.py` / `tests/test_auditor_output_contract.py` — 17 pass.
- `src/agentos/core/auditor_service.py` — audited P8-2 edit preserved.
- `docs/G1_OVERRIDE_AUTHORIZED.md` — G1 preserved.
- `data/agentos.sqlite` — DB evidence=0 preserved.

## Decision required to proceed

The user's instruction explicitly defers implementation: "Prepare the entry checklist ... and do not begin Phase 9 implementation until its scope and prerequisites are verified." This checklist satisfies that; implementation requires a separate authorization/check after prerequisites verified. No Phase 9 code changes made.
