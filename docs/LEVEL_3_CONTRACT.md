# OSS-AgentOS v2.1 — LEVEL 3 CONTRACT (PROMPT 0 — RECONNAISSANCE ONLY)
Status: INSPECT ONLY — NO FILES MODIFIED. Contract only; implementation deferred.

## 1. INSPECTION RESULTS: Level 1 / Level 2
- BUILD_STATE.md: CURRENT LEVEL = LEVEL 2; STATUS = COMPLETE; NEXT = LEVEL 3. Confirmed usable.
- LEVEL_1_REPORT.md: Level 1 COMPLETE (event_store, V001, Session, immutability trigger, role grants).
- LEVEL_2_REPORT.md: Level 2 COMPLETE (org/project/mentor/path/prerequisites/interactions/followups, V002, 7 event types).
- Migrations present and idempotent: V001__init.sql (event_store), V002__mentor_project_path_schema.sql.
- DB access: src/agentos/db/connection.py Session (autocommit=False) + repository.EventStore.append() (atomic batch, rollback on failure).
- CLI: cli.py (typer) + cli_path.py; no evidence/readiness commands exist yet.
- Tests: test_contract.py + unit/integration/cli dirs; integration requires running PostgreSQL (documented, not blocking).
- No LLM/RAG/dashboard/model runtime (Level 0 contract preserved).

## 2. EXISTING SCHEMA & INTERFACES (verified — not invented)
- event_store: PK id UUID DEFAULT gen_random_uuid; aggregate_type/addvarchar(63); aggregate_id UUID; event_type varchar(127); payload JSONB; version bigint IDENTITY; occurred_at timestamptz; source varchar(63). Indexes: PK, unique(aggregate_id,version), (aggregate_type,aggregate_id), (occurred_at). Trigger event_store_immutable (DB layer).
- V002 tables: organizations(id,slug) PK; projects(id,org_id,slug) unique(org,slug); mentors(id,org_id,handle) unique(org,handle); paths(id,org_id,project_id,state CHECK) where state in (WATCH,ENGAGED,ACTIVE,BACKUP,DROPPED); prerequisites(id,path_id,cascade); interactions(id,path_id,direction CHECK(inbound/outbound),level 0-7,link NOT NULL,occurred_at,quote,note) unique(path,link); followups(id,path_id,interaction_id set null,state,due_at) unique(interaction_id).
- Relations: org -> proj/mentor; proj -> path; path -> prereq/interact/followup. No separate path_mentors table; mentor linked via interaction context + evidence.interaction_ref.
- Interfaces: EventStore.append(events); Event.from_dict; Session enter/exit; migrations.run() idempotent via db_migrations registry.

## 3. EVIDENCE SCHEMA PROPOSAL (additive only)
Table evidence (PK id UUID DEFAULT gen_random_uuid; path_id UUID NOT NULL REFERENCES paths(id) ON DELETE CASCADE; claim TEXT NOT NULL; artifact_url TEXT NOT NULL; kind VARCHAR(31) NOT NULL CHECK(kind IN ('fix','test_infra','design','review','community')); depth SMALLINT NOT NULL CHECK(depth BETWEEN 1 AND 5); relevance_to_project NUMERIC(4,3) NOT NULL CHECK(relevance_to_project BETWEEN 0 AND 1); project_specificity NUMERIC(4,3) NOT NULL CHECK(project_specificity BETWEEN 0 AND 1); independence SMALLINT NOT NULL CHECK(independence BETWEEN 1 AND 5); maintainer_signal NUMERIC(3,1) NOT NULL CHECK(maintainer_signal BETWEEN -1 AND 1); mentor_validated BOOLEAN NOT NULL DEFAULT false; understood BOOLEAN NOT NULL DEFAULT false; interaction_id UUID REFERENCES interactions(id) ON DELETE SET NULL; created_at TIMESTAMPTZ DEFAULT now(); updated_at TIMESTAMPTZ DEFAULT now()). Indexes: (path_id,kind); (path_id,mentor_validated); (path_id,project_specificity).
Constraints: all 10 spec fields present; 5 kinds enforced; depth 1-5; relevance/project_specificity 0-1; independence 1-5; maintainer_signal -1..+1; mentor_validated/understood explicit booleans default false.

## 4. PROVENANCE STRATEGY (never infer from activity alone)
R1: evidence.mentor_validated = true AND (evidence.interaction_id -> interactions with verifiable reference OR verifiable artifact_url/reference). Never from contributor claim text.
R2: interactions row with level >= 2 AND interaction.channel = PUBLIC (see 5.2). UNKNOWN never satisfies.
R4: four separate traceable records (not checkbox) — see 5.3.
R5: interactions(level=6 about direction/proposal) OR readiness_assessment record (see 5.4). Assessment need not be positive.

## 5. MISSING PROVENANCE — SMALLEST ADDITIVE CHANGES
5.1 Mentor interaction linkage: evidence.interaction_id (FK to interactions, SET NULL) — smallest change; no new interaction table.
5.2 Interaction channel: interactions currently has direction/level/link/quote/note — NO channel. Add interactions.channel VARCHAR(15) NOT NULL DEFAULT 'UNKNOWN' CHECK(channel IN ('PUBLIC','PRIVATE','UNKNOWN')). UNKNOWN never passes R2 (explicit guard).
5.3 R4 four facts — no generic rules engine. Recommended: readiness_fact table (per §6) rather than 4 bool columns on evidence. If using evidence-only: add evidence_tests_run / evidence_template_followed / evidence_review_round (nullable boolean or reference). Smallest auditable is readiness_fact (one table, FK to path + evidence/interactions/assessment).
5.4 R5 direction: reuse interactions.level=6; if no interaction, add readiness_assessment (path_id, assessment_text NOT NULL, assessed_at). No approval required.

## 6. READINESS FACT REPRESENTATION
Table readiness_fact (PK id UUID DEFAULT gen_random_uuid; path_id UUID REFERENCES paths(id) ON DELETE CASCADE; fact_type VARCHAR(63) NOT NULL CHECK(fact_type IN ('R1','R2','R3','R4_tests','R4_template','R4_review','R5_direction','R5_assessment')); satisfied BOOLEAN NOT NULL DEFAULT false; evidence_ref UUID REFERENCES evidence(id) ON DELETE SET NULL; interaction_ref UUID REFERENCES interactions(id) ON DELETE SET NULL; assessment_ref UUID REFERENCES readiness_assessment(id) ON DELETE SET NULL; recorded_at TIMESTAMPTZ DEFAULT now()). Enables per-requirement audit; correction = new/updated row + event.

## 7. EVENT VOCABULARY (Level 1 event_store only — no second system)
- EVIDENCE_CREATED (aggregate_type='evidence', payload: path_id, evidence_id, claim, kind, depth, ...)
- EVIDENCE_CORRECTED (payload: evidence_id, corrected_fields, prev_values) — for mentor_validated/understood/status changes; old state stays in DB + prior event
- READINESS_FACT_RECORDED / READINESS_FACT_CORRECTED (aggregate_type='readiness', payload: path_id, fact_type, satisfied, refs)
- INTERACTION_CHANNEL_UPDATED (if channel changed) — table update + event
Transaction: Session (autocommit=False): update table + append event(s) in one batch; commit or rollback both; no partial state. Append-only invariant: event_store trigger blocks update/delete on events; table mutations permitted (evidence/readiness updated with new event recorded).

## 8. READINESS OUTPUT (agentos readiness [path])
Print 5-item checklist (not score / not probability):
- R1 Mentor-validated artifact — PASS/UNMET + evidence/interaction refs + missing (e.g., no mentor_validated with interaction_ref)
- R2 Direct technical interaction (level>=2, PUBLIC) — PASS/UNMET + interaction id + missing (channel / level)
- R3 Project-specificity >=0.6 (inclusive) — PASS/UNMET + evidence ids + missing (max <0.6)
- R4 Repository/test/review practices — PASS/UNMET + 4 sub-refs + missing (which unrecorded)
- R5 Project-direction alignment — PASS/UNMET + interaction level-6 id OR assessment ref + missing
First unmet: lowest R-number UNMET (R1→R2→R3→R4→R5). All PASS -> "All five recorded readiness requirements are satisfied." No acceptance probability / 0-100 / confidence / unsupported approval claims.

## 9. SCOPE RESTRICTIONS (NOT implemented)
No ranking, Pareto comparison, watcher, policy registry, Guard, Outbox, approval tokens, GitHub integration, Issue Hunter, LLM, RAG, embeddings, vector DB, quiz, reviewer, sandbox, PR Shepherd, proposal auditor, dashboard. Level 0 FAKE/LOCAL/PAID LLM contract unchanged. No model runtime.

## 10. UNDERSTOOD FIELD
Default false (evidence.understood). Explicit contributor confirmation only (operation = evidence update / CLI confirm-understood; emits EVIDENCE_CORRECTED + updates readiness_fact if linked). Never auto-set from merged PR / passing tests / LLM response. Quiz deferred (later level).

## 11. MIGRATION PLAN (additive after V002; idempotent; CREATE IF NOT EXISTS / ADD COLUMN IF NOT EXISTS)
V003__evidence_schema.sql: CREATE TABLE evidence + indexes; ALTER TABLE interactions ADD COLUMN channel VARCHAR(15) NOT NULL DEFAULT 'UNKNOWN' CHECK(...); optional readiness_fact + readiness_assessment; optional evidence bool columns if chosen over readiness_fact. Preserve V001/V002; register in db_migrations.

## 12. CLI CONTRACT (new; existing unchanged)
agentos evidence add <path_id> claim=... artifact_url=... kind=... depth=... relevance=... specificity=... independence=... maintainer_signal=... mentor_validated=... understood=false [interaction_id=...]
agentos evidence correct <evidence_id> [fields...]
agentos evidence confirm-understood <evidence_id>  (explicit attestation only)
agentos readiness [path_id]  (5-item checklist per §8)
agentos readiness record <path_id> R1/R2/R3/R4/R5 satisfied=<true|false> [evidence_ref=...] [interaction_ref=...] (readiness_fact + event)
Existing: path add/show/state, interact, followup — unchanged.

## 13. TESTING PLAN (pre-change)
Unit: evidence Pydantic validates all constraints; event vocabulary validates payload; readiness engine evaluates R1-R5 correctly; understood never auto-true.
Integration (DB required): V003 migrate; insert path + interaction + evidence; confirm R1-R5; confirm EVIDENCE_CREATED + READINESS_FACT_RECORDED in event_store; rollback test (exception mid-batch) verifies no partial evidence + no partial event.
Red team: R1 with mentor_validated=true but interaction_ref=null and no verifiable URL -> fail; R2 with channel=PRIVATE -> fail; R3 with specificity=0.59 -> fail (0.6 inclusive pass); event update/deletion blocked by trigger; R4 with only claim text -> fail; understood true without confirmation -> fail.

## 14. IMPLEMENTATION ORDER
1. V003 migration (evidence + interactions.channel + readiness_fact/assessment) — additive only.
2. Evidence model + repository + event emission (CREATED/CORRECTED).
3. Readiness engine (evaluate 5 R from DB only; no inference).
4. CLI (evidence add/correct/confirm-understood; readiness; readiness record).
5. Tests (unit + integration design + red team).
6. Update BUILD_STATE.md when authorized.

## 15. ACCEPTANCE CRITERIA
- All 10 evidence fields safely representable; 5 kinds enforced; depth 1-5; relevance/spec 0-1; independence 1-5; signal -1..+1; mentor_validated/understood explicit booleans default false.
- R1 requires mentor_validated=true + traceable interaction/reference (no inference).
- R2 requires interaction level>=2 + channel=PUBLIC (UNKNOWN never passes).
- R3 requires project_specificity >=0.6 inclusive.
- R4 requires 4 separate traceable records; free text alone never passes.
- R5 requires interaction level=6 OR explicit assessment; no approval required.
- understood default false; explicit confirmation only; never auto-set.
- Level 1 event_store only; atomic with DB mutation; rollback no partial state; append-only preserved.
- agentos readiness prints 5-item checklist (ID/status/refs/missing/first-unmet); all-pass confirms 5 satisfied; no score/probability.
- Exclusions respected (no LLM/quz/etc.); Level 0 contract unchanged.

## 16. RISKS / UNRESOLVED (design only — no impl risk yet)
- Integration suite blocked by missing running PostgreSQL (existing Level 1/2 risk).
- Readiness_fact vs 4 evidence bools for R4 — recommend readiness_fact; resolve pre-V003.
- interactions.channel default UNKNOWN means existing rows initially unsuitable for R2 — correct (spec requires explicit PUBLIC).
- evidence.interaction_id optional -> R1 requires engine-level check (inter_ref OR verifiable URL) not just DB constraint.
- No quiz -> understood depends solely on explicit confirmation (correct per spec, but contributor must actively attest).
- Migration idempotency must use existing migrations.py registry and IF NOT EXISTS patterns.
