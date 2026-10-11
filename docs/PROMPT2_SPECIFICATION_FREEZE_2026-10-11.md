PROPOSAL EVIDENCE AUDITOR — FUNCTIONAL SPECIFICATION FREEZE (Prompt 2)
Author: OSS-AgentOS v2.1 plan §2.7 / §6.10; scope freeze docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md (critic-only, never rewrites proposal; depends on inputs; out-of-scope: drafting, policy extractor, L12, PR shepherd, sandbox extension).
Status: SPECIFICATION ONLY — no implementation files edited; no DB writes; proposal/ledger read-only; L11 amendment preserved (not expanded); G1=FAIL; act=OFF; SQLite preserved; uv.lock preserved.
Inputs (owner-confirmed per PROMPT2_INPUT_REGISTRATION_2026-10-11.md + this turn): proposal draft (source per manifest); idea page (source confirmed); chosen size + program hours (confirmed); project mapping (open-os-demo via registry, with proposal_text=BLOCKED flagged); evidence ledger = DB records (0 across evidence/projects/interactions/mentors/hours/log/orgs — preserved empty, not fabricated).

=== 1. RESPONSIBILITIES (from §1 / §6.10) ===
For the input proposal (read-only text/file) plus evidence ledger (read-only SQLite), the component must identify:
- R1 Unsupported claims (claim line + required source quote + timestamp → missing = unsupported).
- R2 Deliverables lacking demonstrated capability or evidence (deliverable listed in proposal / idea page vs evidence ledger entry / external source → missing = unsupported).
- R3 Unvalidated technical assumptions (technical assertion without evidence link or verified source → unknown/unverified; never treated as true).
- R4 Likely mentor challenges (anticipated questions, NOT actual mentor statements; labelled explicitly; not claimed as replies).
- R5 Claims exceeding available evidence (claim strength vs evidence quantity — if evidence=0, ALL capability/delivery claims exceed evidence).
Critic-only: never rewrites, replaces, or generates proposal text. Output = findings + questions + evidence links, never proposal prose.

=== 2. INPUT CONTRACT ===
2.1 Proposal draft
- Source: owner-confirmed file/URL/text (per manifest; registry open-os-demo.yaml proposal_text=BLOCKED noted as inconsistency).
- Validation rules: must be readable text; source identifier recorded (file path / URL + retrieval timestamp); must not be synthetic fixture labelled real; must resolve to same project as idea page (see 2.3).
- Identity: proposal_id = derived from source URL/path + owner-confirmed mapping to open-os-demo / idea page.
- Integrity / consistency: if registry proposal_text=BLOCKED but draft provided → flag contradictory (registry vs draft); if draft source differs from idea page project → flag mismatch; if missing → finding category MISSING_SOURCE.
- Read-only during analysis: file opened read-only; never rewritten.

2.2 Evidence ledger
- Source: SQLite data/agentos.sqlite (existing read-only access: evidence, projects, interactions, mentors, hours_log, organizations, outbox_drafts, approval_tokens tables); audit artifact docs/LEVEL_8_EVIDENCE_LEDGER_AUDIT.md.
- Actual count (verified this session): 0 across all evidence-linked tables.
- Validation: count recorded explicitly; empty = absence of evidence (NOT proof proposal false); never invent records; ingest only with owner authorization + source provenance.
- Reference rules: every finding that references a ledger record must include the table + identifier; if count=0, reference is an explicit EVIDENCE_GAP (not "false").
- Consistency with proposal: compare proposal's referenced entities (projects/mentors/interactions/hours) to ledger IDs — mismatch = CONTRADICTORY; absence = UNKNOWN.

2.3 Idea page
- Source: owner-confirmed (file/URL/description); must reference same project/idea as proposal.
- Validation: readable; source identifier recorded; content sufficient to establish idea scope (not just title).
- Mapping check: if idea project != proposal project → CONTRADICTORY (finding MAPPING_MISMATCH).
- Integrity: if missing → MISSING_SOURCE; if present but empty/unrelated → EMPTY_SOURCE.

2.4 Program hours (chosen project size)
- Source: owner-confirmed (config/programs.yaml + budget/hours sources + maybe DB hours_log); must reference same project.
- Validation: numeric entry-cost figure present; source file/path + timestamp recorded; if DB hours_log=0 and no external source → UNKNOWN (not 0 by assumption).
- Consistency: if proposal implies a size not supported by hours/budget → CONTRADICTORY.

2.5 Cross-source consistency (required — "all inputs refer to same project")
- Rule: proposal source ID, idea source ID, size/hours source, registry org (open-os-demo) must agree on project identifier.
- If any disagree → finding MAPPING_INCONSISTENT (category CONTRADICTORY) with all conflicting sources cited.
- If any missing → finding MISSING_SOURCE for that input; do NOT assume agreement.

=== 3. OUTPUT CONTRACT — FINDING FORMAT ===
Machine-readable; uses existing conventions (similar to evidence ledger event structure / readiness facts). Each finding:
- finding_id: stable (F-{category}-{proposal_ref}-{seq}), e.g. F-UNSUPPORTED-OPENOS-1.
- category: UNSUPPORTED | PARTIALLY_SUPPORTED | MISSING_SOURCE | UNKNOWN | CONTRADICTORY | EVIDENCE_GAP | ANTICIPATED_CHALLENGE (allowed; justified by §4).
- proposal_ref: proposal_id / file line / claim excerpt (max 200 chars; exact substring from proposal, quoted in explanation).
- proposal_location: file_path:line_ref or URL:section (must resolve; if source missing, use EVIDENCE_GAP with source label).
- status: SUPPORTED | PARTIALLY_SUPPORTED | UNSUPPORTED | UNKNOWN | CONTRADICTORY | MISSING_SOURCE. (Distinct; additional allowed only with justification — none needed here.
- explanation: 1–3 sentences; cites source (file/line/DB table:row-key or EVIDENCE_GAP); quotes supporting or missing evidence as substring; never asserts false negative; distinguishes unavailable from checked-no-evidence.
- evidence_links: list of {table:file_id | file_path:line | DB:table:id | URL:...}; empty if EVIDENCE_GAP; must resolve to actual source (not invented IDs).
- evidence_gap: explicit statement when evidence missing ("ledger table X count=0; source Y unreadable"); NOT silent omission.
- question / validation_action: concrete ("Confirm mentor reply at URL..." / "Provide evidence link for claim..." / "Confirm project mapping...").
- mentor_challenge_label: ANTICIPATED_CHALLENGE (not actual mentor reply); always explicit.
- proposal_rewrite_check: PASS (no proposal text replaced) — verified per output generation.

Status semantics (required, distinct):
- SUPPORTED: claim + evidence link + timestamp, all same project, no contradiction.
- PARTIALLY_SUPPORTED: some evidence exists but incomplete or partial project match.
- UNSUPPORTED: claim made + evidence missing / contradictory / unverified; never "false" — only "not supported by available evidence".
- UNKNOWN / UNVERIFIED: source unavailable or evidence unverified; must not become negative factual conclusion.
- CONTRADICTORY: sources disagree (e.g., registry BLOCKED vs draft provided; idea project != proposal; size expenditure vs budget).
- MISSING_SOURCE: required input (draft/idea/hours/ledger entry) absent.
- EVIDENCE_GAP: evidence checked and found absent (e.g., DB count=0 for relevant table); explicit.

=== 4. ARCHITECTURE & SAFETY ===
4.1 Reuse / module placement
- CLI entry: new `cli_auditor.py` (or extension of `src/agentos/cli.py` / `cli_next.py`) — register under existing Typer app; no new providers/models without approval.
- DB access: existing `src/agentos/db/repository.py` + `sqlite3` read-only; use existing connection patterns (`data/agentos.sqlite`); NO new DB; NO writes to event_store/evidence/hours during analysis.
- Evidence ledger read: `src/agentos/db/evidence_repo.py` pattern (if available) or direct `sqlite3` SELECT; read-only transaction.
- Input loaders: file read + `py -3` / standard lib; no external fetch without approval; if web URL needed, use `httpx` (existing dependency via `pyproject.toml`) with conditional request / ETag; document if used.
- Validation: `Pydantic v2` (existing) for finding structure; schema defined in this spec; enum for category/status.

4.2 Read-only enforcement (security / boundary)
- Proposal file: opened `r` (text); never `w`; checksum/hash optional for integrity (not required here; registry BLOCKED noted as discrepancy not corruption).
- Ledger DB: open with `uri?mode=ro` or read-only `sqlite3` connection; verify `SELECT` only; no `INSERT/UPDATE/DELETE`; if ingestion authorized separately (not in this spec), separate write path must require explicit authorization.
- No model-provider writes; no publication / Outbox / L3 action from auditor.
- Untrusted input isolation: proposal text treated as untrusted data (per AGENTS.md §7); structured-output validation ensures no proposal text appears in finding fields except quoted substrings (≤200 chars) with line refs; unsupported model assertions must be labelled `UNCERTAIN` and rejected if unverified.

4.3 If semantic analysis uses a model (documented, not required here)
- Input isolation: proposal text passed only to isolated read-only analyst context (no secrets, no tool access, no DB writes).
- Structured output: validated against Pydantic schema (category/status/explanation/evidence_links) — zero out-of-enum fields; zero unquoted proposal text inserted.
- Unsupported assertions: any model-produced claim without evidence link must be rejected or labelled `UNCERTAIN`; never promoted to `SUPPORTED` by model alone; ledger evidence (or its absence) is authoritative.
- Since current scope is critic-only against explicit inputs + empty ledger, primary mode is deterministic (string matching / source comparison / DB count); model use only if owner later authorizes semantic analysis — documented here, not activated.

=== 5. ACCEPTANCE MATRIX (traceable) ===
Req / Behavior / Implementation location / Test / Failure condition
R1 find unsupported claims → output findings with UNSUPPORTED status, quoted claim, missing evidence link → `src/agentos/cli_auditor.py` / `domain/auditor_finding.py`; test verifies UNSUPPORTED when DB=0 / source missing → FAIL if claim rated SUPPORTED with evidence=0.
R2 missing capability / evidence → finding MISSING_EVIDENCE with evidence_gap=DB:table=0 → same → FAIL if deliverable treated as demonstrated without ledger entry.
R3 unvalidated assumptions → finding UNKNOWN with explanation noting assumption unverified → same → FAIL if treated as SUPPORTED.
R4 mentor challenges → finding ANTICIPATED_CHALLENGE with label; no actual mentor reply required → same → FAIL if presented as actual mentor statement.
R5 exceed evidence → finding UNSUPPORTED / EVIDENCE_GAP when claim > available evidence count → same → FAIL if claim rated SUPPORTED with 0 evidence rows.
Input identity → proposal_id derived from source + mapping check against idea page + registry → same → FAIL if sources disagree with no CONTRADICTORY finding.
Cross-source consistency → MAPPING_INCONSISTENT finding when draft/idea/size project differ → same → FAIL if inconsistency ignored.
Read-only proposal / ledger → connection mode verified; SELECT only; file open r → `tests/test_auditor_readonly.py` → FAIL if any write/log mutation detected.
Output format / schema → all findings pass Pydantic validation; no out-of-enum category/status; evidence_links resolve → schema tests → FAIL on invalid finding.
Critic-only / no proposal rewrite → output checked: zero proposal prose replacement; only quoted substrings (≤200 chars) with line refs → test asserts → FAIL if proposal text altered.
Ledger empty handled → findings include EVIDENCE_GAP with DB counts; never synthetic records → test with DB=0 → FAIL if fabricated ledger rows appear.
Mentor reply not required → no finding requires mentor interaction; ANTICIPATED_CHALLENGE only → test → FAIL if mentor reply treated as mandatory.
L11 / amendments preserved → no auditor code modifies L11 docs/DB/gates; amendment scope not expanded → verification → FAIL if amendment edited / L12 started / G1 rewritten.

=== 6. SCHEMA (Pydantic v2 — proposed, not fully implemented) ===
class FindingStatus(str, Enum): SUPPORTED="supported"; PARTIALLY_SUPPORTED="partially_supported"; UNSUPPORTED="unsupported"; UNKNOWN="unknown"; CONTRADICTORY="contradictory"; MISSING_SOURCE="missing_source"; EVIDENCE_GAP="evidence_gap"
class FindingCategory(str, Enum): UNSUPPORTED="unsupported"; PARTIALLY_SUPPORTED="partially_supported"; MISSING_SOURCE="missing_source"; UNKNOWN="unknown"; CONTRADICTORY="contradictory"; EVIDENCE_GAP="evidence_gap"; ANTICIPATED_CHALLENGE="anticipated_challenge"
class EvidenceLink(BaseModel): kind: Literal["db","file","url","registry"]; reference: str; location: str; verified: bool
class Finding(BaseModel): finding_id: str; category: FindingCategory; proposal_ref: str (max 200); proposal_location: str; status: FindingStatus; explanation: str (max 2000); evidence_links: List[EvidenceLink]; evidence_gap: Optional[str]; question: Optional[str]; mentor_challenge_label: Optional[str]; proposal_rewrite_check: Literal["pass"]; source_timestamp: Optional[str]
Constraints: explanation must contain at least one quoted substring or explicit EVIDENCE_GAP statement; evidence_links empty only when evidence_gap set; mentor_challenge_label present only when category==ANTICIPATED_CHALLENGE.

=== 7. REFERENCES TO ACTUAL SOURCE (verified, not invented) ===
- Proposal draft source: owner-confirmed (per manifest) — registry/open-os-demo.yaml proposal_text=BLOCKED noted as discrepancy.
- Evidence ledger: SQLite data/agentos.sqlite (tables verified: evidence/projects/interactions/mentors/hours_log/organizations/outbox_drafts/approval_tokens; counts=0).
- Idea page: owner-confirmed source (per manifest; not synthetic).
- Hours/size: owner-confirmed (per manifest; DB hours_log=0 preserved; config/programs.yaml no size field noted).
- Plan references: AGENTS.md §1/§4/§7/§14; original plan §2.7 / §6.10; scope freeze docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md.
- L11 preservation: docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md (§2.2 NOT MET); docs/LEVEL_11_CLOSURE_GATE_ACCEPTANCE_REPORT.md (Sec 9 gap named); sandbox/stage_a/dependency_workflow_completion_2026-10-11.md.
- No claims made about proposal content (draft not reproduced); no synthetic evidence links; no fabricated DB IDs.

=== 8. GATE / NEXT ===
Specification freeze complete. No implementation edited (no `cli_auditor.py`, no DB schema change, no module). No model invoked (deterministic design). No proposal prose rewritten.
Awaiting owner authorization of this spec before Prompt 3 (implementation) begins. If authorized, next: implement `Finding`/`EvidenceLink` schemas + `cli_auditor` read-only entry + DB read + extraction of quoted claim substrings + output to structured format — all within read-only / critic-only / L11-preserved constraints.
