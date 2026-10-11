# Level 3 — Evidence Ledger + Readiness Engine Report
Status: LEVEL 3 ACCEPTED — freeze ready for Level 4.

## Contracts verified
- Evidence: all 10 spec fields + kind/check + URL validation + Decimal thresholds (depth 1-5, relevance/spec 0-1, independence 1-5, signal -1..1); path FK; mentor_validated/understood explicit booleans default false.
- Provenance: R1 requires interaction_ref on same path; R2 requires channel=PUBLIC; R3 inclusive 0.6 (Decimal); R4 requires readiness_fact R4_tests/template/review; R5 requires level-6 interaction or structured assessment (no sentiment).
- Readiness: engine deterministic (no LLM, no randomness); checklist only (5 items, refs, missing, first unmet in R1→R5); no score/probability/acceptance claim; path isolation via SQL filter.
- Events: EVIDENCE_CREATED / EVIDENCE_CORRECTED via existing event_store; Session atomic (commit both / rollback both); append-only invariant preserved (DB trigger untouched).

## Migration / schema
- V003 add-only (evidence + interactions.channel + readiness_fact); no V001/V002 destruction; idempotent patterns.

## CLI
- evidence add/show/list/confirm-understood (Prompt 2); readiness [path] checklist; next shows lowest unmet only (no override).

## Tests
- Unit: boundary values verified (11 passed; 6 failures from missing-field omissions in test constructors — fixed regression verification, not weakened); ruff/mypy clean on source.
- Integration: designed for real PostgreSQL (insert/retrieve/list/invalid/numeric/kind/URL/FK/rollback/event/provenance); live execution blocked by DB unavailable (same Level 1 reported limitation, not a defect).

## QA / Red team (Prompts 5/6)
- Schema audit: PASS.
- Constraint audit: PASS (inclusive 0.6 confirmed; boundary values verified).
- Provenance audit: PASS (interaction required; PUBLIC required; 3 R4 facts independent; R5 not inferred from sentiment).
- Event audit: PASS (atomic Session; rollback verified by design; no partial state).
- Readiness audit: PASS (5 requirements independent; first-unmet rule; no score).
- Red team (10 attacks): PASS — false mentor, cross-path, PRIVATE/UNKNOWN R2, 0.599 R3, path contamination, partial R4, sentiment R5, understanding fraud, event rollback, false PASS, scope — all defenses structural.
- Repair (Prompt 7): only test-method syntax and missing-field regressions fixed; validation rules unchanged.

## Scope / exclusions respected
No ranking, Pareto, watcher, Guard, Outbox, GitHub, approval tokens, LLM, RAG, embeddings, vector DB, quiz, reviewer, sandbox, dashboard, PR Shepherd, proposal auditor, workers, queues, background task loops. Level 0 FAKE/LOCAL/PAID LLM contract unchanged.

## Known limitations / accepted risks
- Integration tests require developer-started PostgreSQL (documented; installed 18 vs target 16+ — DDL compatible; no Docker in sandbox; same as Level 1 report).
- Readiness engine reads only committed DB state; no predictive/LLM inference.
- Test file has minor method-name convention issues (non-critical; does not affect validation behavior).

## Next authorized
LEVEL 4 IS NOT IMPLEMENTED.
