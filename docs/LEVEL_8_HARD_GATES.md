# LEVEL 8 — SEVEN HARD GATES (DATA CONTRACT ONLY — NO ENGINE)
Prepared: 2026-10-10 (G1_OVERRIDE_AUTHORIZED; G1 FAIL unchanged)
Status: DESIGN / CONTRACT — gates defined; execution deferred to live DB + verified evidence
Precondition: G1_OVERRIDE_AUTHORIZED.md exists; G1 not edited to PASS; no fabricated evidence.

## Rule set preserved (non-negotiable)
- Deterministic: policy / eligibility / gate results use source-defined rules; LLM does not override.
- Evidence-required: unknown data stays UNKNOWN; never treated as passing.
- Exclusion preserved: excluded paths kept; explanation recorded; no deletion.
- Rolling 30-day preserved (budget/time); calendar-month not introduced.
- Safety: no automatic upstream; Guard / approval / kill-switch / budget / FAKE-LOCAL-PAID preserved.

---

## GATE 1 — PROGRAM ELIGIBILITY
Rule: Source-defined eligibility for intended program / cycle. Unknown = UNKNOWN (not PASS).
Evidence: program_config / registry / source spec (PDF unavailable — provisions from existing files).
Validation: match candidate profile against program rules.
Missing: eligibility unverified for 8 (G0); source dates not assumed for future cycles.
Result behavior: PASS (verified), FAIL (verified ineligible), UNKNOWN (not verified — preserved).

## GATE 2 — REGISTRY AND CONTACT
Rule: Effective policy mode ≥ UNDERSTANDING_ONLY (source-defined) AND known contact.channel.
Evidence: existing deterministic policy-registry calculation; registry file; contact evidence.
Validation: policy mode computed deterministically; contact.channel present and not stale.
Unknown/stale policy: NOT treated as permission; result = FAIL / BLOCKED with explanation.
Result behavior: PASS (mode ≥ threshold + contact known), FAIL (mode insufficient / contact missing / stale), BLOCKED (unknown — do not infer permission).

## GATE 3 — ACTIVE CONTRIBUTION ACCEPTANCE
Rule: Verifiable evidence of merged PR / contribution within preceding 30 days (from fixed clock).
Evidence: evidence ledger; git / API / fixture; actual merged PR not repository activity proxy.
Validation: contribution within 30-day window; date-bound; source-defined acceptance criteria.
Missing/unknown: no evidence = UNKNOWN (not PASS); arbitrary repo activity ≠ contribution acceptance.
Result behavior: PASS (dated merged PR within 30d), FAIL (none / rejected / outside window — explanation preserved), UNKNOWN (evidence not yet verified).

## GATE 4 — SOCIAL RESTRICTIONS
Rule: Exclude path when SOCIALLY_RESTRICTED blocker applies to relevant contribution area.
Evidence: source / registry / policy evidence (verified — never invented).
Validation: blocker applies to contribution area; evidence cited.
Result behavior: EXCLUDE (reason + evidence preserved); PASS (no blocker for area); UNKNOWN (blocker status unverified — do not treat as absence).

## GATE 5 — FEASIBLE TIME
Rule: Estimated entry cost vs available evidence hours before applicable milestone.
Evidence: calendar / cli_hours / evidence log (actual records); fixed clock for date-sensitive tests.
Validation: cost ≤ available hours before milestone; no invented hours.
Missing: unknown available hours = UNKNOWN (not PASS); milestone source-defined.
Result behavior: PASS (feasible), FAIL (infeasible — explanation + evidence), UNKNOWN (hours / milestone missing).

## GATE 6 — ACHIEVABLE PREREQUISITES
Rule: Source-defined max catch-up estimate = 20 hours (threshold NOT changed; labeled estimate).
Evidence: prerequisite assessment; estimate clearly labeled.
Validation: estimated catch-up ≤ 20h; if >20h = FAIL / BLOCKED with explanation.
Unknown: not changed to pass.
Result behavior: PASS (≤20h), FAIL (>20h — label estimate; preserve explanation), UNKNOWN (assessment missing).

## GATE 7 — MENTOR AVAILABILITY (date-sensitive; fixed-clock tests)
Rule (source-defined, preserved exactly):
- At least one identifiable reviewer responded to a newcomer issue or PR within preceding 14 days (from clock);
- At least one qualifying response observed during preceding 90 days.
Evidence: dated evidence ledger / issue/PR comments (verifiable — not inferred from repo activity alone).
Validation: dates within windows; reviewer identifiable; response to newcomer; not fabricated.
Unknown: response unobserved = UNKNOWN (not PASS); repo activity ≠ response.
Result behavior: PASS (both windows satisfied with dated evidence), FAIL (windows not met — explanation + missing evidence), UNKNOWN (evidence incomplete / DB deferred — fixtures only).

---

## RESULT CONTRACT (per gate)
For each evaluation return:
- STATUS: PASS / FAIL / UNKNOWN / BLOCKED / EXCLUDE (per gate rule above)
- HUMAN-READABLE REASON (source-linked; no invented explanations)
- SUPPORTING EVIDENCE (file / URL / evidence-ID / fixture reference)
- OBSERVATION DATE (fixed clock for test; actual for live)
- MISSING-DATA EXPLANATION (explicit — never hidden; never converted to PASS)

---

## EXCLUSION BEHAVIOR (preserved)
Excluded paths (e.g. Gate 4 SOCIALLY_RESTRICTED) are preserved with explanation; not deleted from comparison. Feature vector for excluded paths may record blocker; sortable / Pareto comparison excludes them per source rule.

---

## TESTS (design / contract-level; execution deferred due to DB deferred — documented)
- Each gate independently (single failure per gate; confirm status reflects only that gate).
- Multiple simultaneous failures (aggregate status; explanations preserved separately).
- Unknown inputs (each gate returns UNKNOWN; no invented evidence pushes to PASS).
- Stale evidence (date window excludes; explanation preserved; no inference from presence of repo).
- Time boundaries (14d / 30d / 90d / milestone; fixed clock; boundary inclusive/exclusive per source rule preserved — not changed).
- Policy restrictions (Gate 2 / 4; deterministic; LLM override not permitted).
- Exclusion explanations (Gate 4; preserved with evidence citation).
- Suitability: fixtures / test doubles for DB-deferred environment; no live upstream changes.

---

## MISSING / DEFERRED (documented)
- Full gate execution vs live evidence ledger deferred (DB 5432 timeout — fixture/test-double only).
- Mentor-date verification requires dated evidence (fixture when DB unavailable); not fabricated.
- Contribution 30d verification requires actual merged-PR evidence (fixture / test double when DB deferred); repo activity not substituted.
- Per-candidate eligibility unverified (G0); unknown preserved.
