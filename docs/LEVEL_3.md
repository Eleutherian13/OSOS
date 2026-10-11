# Level 3 — Evidence Ledger (Prompt 1 — implemented; not complete)

Status: EVIDENCE FOUNDATION IMPLEMENTED. READINESS ENGINE NOT YET IMPLEMENTED (next prompt).

## Schema (V003 — additive, idempotent)
- evidence (path_id FK paths cascade; claim; artifact_url; kind CHECK; depth 1-5; relevance_to_project/project_specificity numeric 0-1; independence 1-5; maintainer_signal -1..1; mentor_validated bool default false; understood bool default false; interaction_id FK interactions set null; created_at/updated_at)
- interactions.channel added (PUBLIC/PRIVATE/UNKNOWN; default UNKNOWN; UNKNOWN never satisfies R2)
- readiness_fact (path_id, fact_type R1-R5 subtypes, satisfied bool, evidence_ref, interaction_ref, recorded_at)

## Validation enforced (app boundary + DB second line)
- Numeric ranges tested at boundaries (1/5, 0/1, 0.6, 1-5, -1/0/1); Decimal used for threshold logic (no float-comparison errors)
- Kind: exactly fix/test_infra/design/review/community; arbitrary strings rejected
- URL: https/http required; arbitrary prose rejected; not fetched/verified
- Path existence required; interaction on same path required when mentor_validated=true (never inferred)
- Understood default false; explicit confirm-understood only (no auto-set from test/PR/LLM)

## Provenance (Prompt 0 contract preserved)
- R1: mentor_validated + supporting interaction_ref (same path) or verifiable URL
- R2: interaction.level >=2 and interaction.channel = PUBLIC
- R3: project_specificity >= 0.6 (inclusive)
- R4 / R5: readiness_fact + interaction level-6 / assessment records (no inference)

## Events / transactions
- EVIDENCE_CREATED + EVIDENCE_CORRECTED via existing event_store (aggregate_type=evidence)
- Evidence mutation + event commit atomically through Session (autocommit=False; rollback on failure; no partial state)
- Append-only invariant preserved (event_store trigger + role grants unchanged)

## CLI (Prompt 2 — not yet implemented)
- agentos evidence add / show / list / confirm-understood planned; readiness engine deferred

## Tests
- Unit: boundary values for all numerics, kind rejection, URL validation, understood default
- Integration design: real PostgreSQL required; covers insert/retrieve/list/invalid-path/invalid-numeric/invalid-kind/malformed-URL/foreign-key/transaction-rollback/event-creation/provenance (DB unavailable at test time — documented in LEVEL_1_REPORT style)
