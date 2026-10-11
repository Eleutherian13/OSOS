# LEVEL 8 — RANKING DATA CONTRACT
Prepared: 2026-10-10 (override authorized; G1 remains FAIL; not a G1 PASS claim)
Status: DESIGN ONLY — no ranking engine implemented
Precondition verified: docs/G1_OVERRIDE_AUTHORIZED.md exists; G1 not edited to PASS.

## 1. Purpose (decision support, not prediction)
Ranking supports comparative evaluation of contribution paths using verifiable evidence. No overall opportunity score. No predicted probability of acceptance. No automatic upstream changes.

## 2. Separation of concerns (preserved)
| Layer | Content | Source / rule |
|---|---|---|
| Hard eligibility gates | PASS / FAIL / UNKNOWN / BLOCKED (per source) | Source-defined rules (see LEVEL_8_HARD_GATES.md) |
| Descriptive feature vector | Observed evidence fields only; each annotated | Registry, evidence ledger, calendar, policy registry |
| Pareto comparison | Non-dominated path identification (optional) | Feature vector only; no score synthesis |
| Optional deterministic sort | Sort key explicit, reversible; not a score | User-defined or source-defined key |
| Readiness / next-action | Per-path guidance with evidence citations | Evidence ledger + milestone calendar |

## 3. Feature sources (provenance required; no inference)
| Feature | Authoritative field | Source / reference | Observation | Status if missing |
|---|---|---|---|---|
| Program eligibility | program_config / eligibility rules | Source spec (not PDF available — provisions from existing files) | Unknown if not verified | UNKNOWN — not assumed |
| Registry / effective policy | policy_registry effective_mode | Existing policy-registry calculation | Actual fetch / config | Must be ≥ UNDERSTANDING_ONLY |
| Contact channel | contact.channel | Registry / evidence | Verified or unknown | Unknown = gate 2 not passed |
| Contribution acceptance (30d) | merged PR / commit evidence | Evidence ledger / git / API (fixture when DB deferred) | Preceding 30 days from clock | Unknown = gate 3 not passed |
| Social restriction | SOCIALLY_RESTRICTED blocker | Source / registry / policy evidence | Verified or absent | Verified = exclusion (preserved) |
| Feasible time | evidence_hours + calendar milestone | cli_hours / calendar / evidence log | Actual records | Unknown = gate 5 not passed |
| Prerequisites catch-up | max 20h (source-defined) | Source rule | Estimate labeled | Estimate = estimate; not changed |
| Mentor response (14d/90d) | identifiable reviewer response (dated) | Evidence ledger / issue/PR comments | Dated within windows | Unknown = gate 7 not passed |

## 4. Data provenance rules (per feature)
- Authoritative field named above; no substitution.
- Source reference recorded per feature (file / URL / config / evidence ID).
- Observation timestamp recorded (actual clock; fixed clock for date-sensitive tests).
- Status: observed / estimated / unknown — never inferred from absence.
- Validation: source rule applied deterministically (no LLM override).
- Missing data: feature = UNKNOWN; does NOT become PASS; exclusion preserved.

## 5. Program adapters (reuse)
Reuse existing program_config / adapter interface. Keep program-specific rules separate (GSoC vs ASF vs CNCF etc. where source defines them). Do not assume old program dates apply to future cycles. No new adapter unless interface genuinely missing.

## 6. Missing inputs (documented; not invented)
- Original spec PDF unavailable — provisions from BUILD_STATE / LEVEL_7_REPORT / existing contracts used.
- Per-candidate eligibility — not verified for 8 (G0 base); unknown preserved.
- Manual baseline time — not measured; time-comparison feature unavailable.
- AI-use policies / newcomer responses / 10-item relevance — 0/8 verified.
- DB live — deferred; evidence ledger uses fixtures/test doubles.
- Per-agent cap / blackout / deadline — sources missing (documented).

## 7. Tests (design-level; full execution deferred to DB integration)
- Contract test: each feature source points to real file/config/reference (no dangling references).
- Provenance test: every feature carries observation timestamp + status label.
- Unknown-handling: missing input produces UNKNOWN, not PASS; no fabricated evidence.
- Gate coupling: feature vector does not override hard-gate result.
- Safety: no automatic upstream; no scalar score produced; rolling 30-day preserved.

## 8. Not implemented (preventing scope creep)
- Ranking engine (no compute path).
- Overall score / probability (explicitly excluded by rules).
- Hard gates (separate file LEVEL_8_HARD_GATES.md).
- Evidence ingestion pipeline (DB deferred; fixtures only).
- Automatic upstream writes / outbound messages.
