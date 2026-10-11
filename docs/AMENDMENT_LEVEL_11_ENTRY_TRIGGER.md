# AMENDMENT: LEVEL 11 ENTRY TRIGGER WAIVER (2026-10-11)

**Document ID:** AMENDMENT-2026-10-11-LEVEL11-ENTRY  
**Date:** 2026-10-11  
**Authority:** Explicit Owner Direction (Precedence Level 1, `AGENTS.md` §1)  
**Subject:** One-time Waiver of Conditional Entry Trigger for Level 11 Sandbox Only  
**Status:** `ADOPTED AND BINDING`

---

## 1. Context and Origin

Under the original `OSS-AgentOS-v2.1-Implementation-Plan.md.pdf` (§§6.7, 13.2) and `AGENTS.md` §4, the Sandbox subsystem is defined as conditional:
> *"Sandbox: only when the configured workflow mode is `COPILOT` or safe code reproduction/testing is a measured bottleneck. If neither condition holds, do not treat Sandbox as the automatic next step."*

During baseline measurements and Level 11 entry evaluations, the empirical status of these triggers was recorded:
1. **`workflow_mode == COPILOT`:** **`NOT MET`** (the system operates in autonomous/interactive analysis mode, not COPILOT).
2. **Measured reproduction / testing bottleneck:** **`NOT MET`** (`ripgrep` and local inspection baseline was sufficient).

On 2026-10-11, following runtime container installation and verification progress, the project owner explicitly selected **Option A**: formally waive the conditional entry requirement for Level 11 only, authorizing the completion and acceptance verification of the Level 11 Sandbox subsystem.

---

## 2. Operative Provisions

1. **One-Time Scope-Limited Waiver:**
   The requirement that `workflow_mode == COPILOT` or that a measured reproduction bottleneck exist is hereby waived **strictly and exclusively for the Level 11 Sandbox subsystem**.

2. **Historical Trigger Facts Unchanged:**
   Both historical trigger results remain **`NOT MET`**. This amendment does not rewrite historical records, gate outcomes, or baseline measurements.

3. **Strict Non-Expansion of Scope:**
   - This amendment does **NOT** alter the active workflow mode.
   - This amendment does **NOT** alter `G1 = FAIL` or expand `G1_OVERRIDE_AUTHORIZED`.
   - This amendment does **NOT** authorize Level 12 (Context Engine / Dossier), policy extractor LLMs, or any deferred subsystems.
   - The conditional subsystem rules in `AGENTS.md` §4 remain fully applicable to all other conditional components.

4. **Technical Acceptance Safeguards Retained:**
   This waiver applies solely to the **entry trigger gate**. It does **NOT** waive any technical, security, isolation, or testing requirements for Level 11 acceptance. Stage A dependency prefetch and Stage B isolation controls must be verified with genuine evidence.

5. **Rationale:**
   The owner has explicitly directed completion, verification, and freeze of the sandbox implementation already initiated and tested on the host runtime.

---

## 3. Precedence and Binding Effect

Per `AGENTS.md` §1 (*"The owner's latest explicit decision, but only for the decision it actually changes"*), this amendment is formally incorporated into the repository contract as an accepted amendment to the v2.1 plan.
