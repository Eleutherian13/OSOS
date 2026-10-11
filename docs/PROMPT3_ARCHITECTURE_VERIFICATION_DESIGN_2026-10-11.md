PROPOSAL EVIDENCE AUDITOR — ARCHITECTURE & VERIFICATION DESIGN (Prompt 3 prep)
Status: DESIGN ONLY. No source edited (cli_auditor.py absent; DB schema unchanged; L11/AGENTS.md/uv.lock preserved; G1 preserved; act=OFF).
Inputs (owner-confirmed per previous turn): proposal draft; idea page; size+hours; open-os-demo registry (proposal_text=BLOCKED noted); ledger=0 preserved.

=== PHASE A — ACTUAL ARCHITECTURE (verified, not filenames) ===
CLI: Typer (`cli.py`); subcommands (`cli_hours`, `cli_issue_hunter`, `cli_path`, `cli_rank`, `cli_readiness`, `cli_sandbox`, etc.) register on `app`. New auditor registers as `cli_auditor.py` importing `app` or separate `typer.Typer`; no new provider needed.
DB: SQLite `data/agentos.sqlite` (verified; 19 tables; V012 event trigger; NOT PostgreSQL — `connection.py` doc references psycopg but repository uses SQLite per AGENTS.md §5 / owner decision). Read access via `sqlite3` or `connection.execute()`; evidence repo (`evidence_repo.py`) validates `Evidence` model (kind/depth/relevance/independence) — pattern reusable for audit findings.
Schema / model: `models.py` defines Pydantic v2 `Event` (id, occurred_at, aggregate_type, aggregate_id, event_type, payload, payload_schema) — audit findings can use same event-style persistence if later required, or separate `Finding` schema (defined in spec freeze) without altering event store.
Evidence access: `evidence_repo.py` (`EvidenceRepo.add/get`) validates URLs/depth/relevance; for auditor, read-only SELECT on `evidence` table + related (`projects`, `interactions`, `mentors`) via existing `repository.py` / direct `sqlite3`.
Config / dependencies: `pyproject.toml` / `uv.lock` (preserved). No new package needed for deterministic mode (string/DB comparison); if semantic analysis authorized later, `httpx` (existing) for conditional fetch; model provider only if owner explicitly approves (not now — per AGENTS.md §7 / §4 / spec freeze §4.3).
Source handling: proposal/idea pages read as text (standard `open()`); no execution; proposal text never executed; untrusted input isolation (AGENTS.md §7 prompt-injection architecture: extract typed facts first, then analyst, then validation — applied here by extracting quoted substrings + DB IDs before any judgment).
Logging / errors: `errors.py` (`DatabaseConnectionError`, `UnknownDatabaseDriver`); use existing; audit errors surfaced as `UNKNOWN` findings, not silent omissions.
Tests: `tests/unit/`, `tests/cli/`; `pytest` used; fixture patterns existing (`tests/test_contract.py`, `test_level11_sandbox_orchestrator.py`); synthetic fixtures labeled (per AGENTS.md §6 / spec freeze §4.2).

=== PHASE B — DATA FLOW ===
1 Load inputs (read-only): proposal file/text; idea file; hours/config; DB SELECT evidence/projects/interactions/mentors/hours.
2 Validate identity: compare source IDs + registry (`open-os-demo.yaml`) + DB project IDs; flag MAPPING_INCONSISTENT if disagree.
3 Extract claims (deterministic): scan proposal text for claim markers (deliverables / technical assertions / capability claims); quote exact substring (≤200 chars) + line/file reference; NO semantic replacement.
4 Associate evidence: for each claim, query DB (projects/interactions/mentors/evidence) by relevant IDs; if 0 rows → EVIDENCE_GAP with counts (not "false").
5 Evaluate strength (partly deterministic, partly semantic): count evidence links / depth / relevance; if ≥1 verified link → PARTIALLY_SUPPORTED or SUPPORTED (if full); if 0 → UNSUPPORTED / EVIDENCE_GAP; if contradictory sources → CONTRADICTORY.
6 Unvalidated assumptions (semantic judgment — documented, isolated): any technical assertion without DB link labeled UNKNOWN; if model used (only with approval), output validated against schema; unsupported model assertions rejected / UNCERTAIN.
7 Anticipated mentor challenges (explicit label ANTICIPATED_CHALLENGE; never actual reply; never required input): derived from proposal's weakest claims / missing evidence / contradiction points.
8 Validate finding: Pydantic schema check (category/status/explanation/evidence_links/quoter); source references must resolve (if DB count shown, must match; if file ref, path must exist).
9 Structured output + metadata: findings written to file/stdout (read-only source preserved); execution log records input sources + DB counts + timestamp (no proposal mutation).
Distinction: deterministic (identity check, DB count, quote extraction, schema validation, contradiction detection when sources disagree) vs semantic (claim interpretation, strength grading, challenge anticipation — isolated, labelled uncertain if model-assisted, never sole basis for SUPPORTED).

=== PHASE C — TRUST BOUNDARIES ===
Untrusted: proposal text, idea text, evidence DB content, model output, repository source files.
Instruction-injection defense (AGENTS.md §7, §12): proposal text never executes; never passed to tool-capable worker unvalidated; quoted substrings extracted deterministically first; any instruction-like prose in draft is LOGGED (as claim context) but never executed; schema validation rejects unexpected fields.
Model-output isolation (spec freeze §4.3): if model used (future, approved only), analyst has no secrets/no DB writes; output fed through Pydantic validator; unsupported assertions rejected; zero out-of-enum fields; proposal text never inserted into output except quoted substrings with refs; unclear judgments labelled UNCERTAIN.
Source verification: each evidence_links entry resolves to actual DB row/file line/URL; if DB count=0, link is EVIDENCE_GAP (explicit); missing source = MISSING_SOURCE; contradiction = CONTRADICTORY.
Stale / malformed / conflicting: proposal claims stale relative to idea page → CONTRADICTORY; evidence record malformed (bad URL/depth) → ignored + EVIDENCE_GAP; conflicting registry vs draft → CONTRADICTORY; partial failure (some claims evaluated, others blocked by missing input) → report includes both evaluated and blocked sections; never produces misleadingly complete report.
Read-only enforcement: proposal/idea opened 'r'; DB connection read-only (`sqlite3.connect('...')` with no writes; `execution_options` or explicit SELECT-only); audit never calls `add()` on `EvidenceRepo`; any attempted write raises / is rejected by design.
Secrets / external calls: no API keys in auditor; no outbound calls unless explicit `httpx` fetch approved (conditional, with ETag); no `curl | sh`; no host execution of proposal code; `act=OFF` preserved.

=== PHASE D — VERIFICATION MATRIX ===
Unit (pytest, synthetic fixtures labeled):
- input_validation: proposal load (read-only), idea load, DB SELECT count, mapping check. Pass: inputs load; DB untouched; mapping correct. Fixture: synthetic proposal snippet (labelled SYNTHETIC).
- classification_boundary: UNSUPPORTED vs EVIDENCE_GAP vs CONTRADICTORY with DB=0 vs contradictory registry. Pass: correct category; explanation contains quote or gap statement.
- finding_construction: Pydantic validates Finding; proposal_rewrite_check=pass; explanation has quote/gap; evidence_links resolve or gap set.
- output_validation: all findings pass schema; zero out-of-enum; zero proposal prose replacement.
Integration (existing patterns):
- sqlite_access: `data/agentos.sqlite` SELECT evidence/projects/interactions/mentors; count matches DB; no write detected (check file mtime/sha pre/post).
- cli_invocation: `python -m agentos.cli_auditor` (proposed) with `--proposal`, `--idea`, `--hours`; exit 0; output valid JSON / structured.
- evidence_ref_resolution: DB IDs from findings match actual rows; file refs exist; URL refs valid (if used).
- report_gen: structured output contains finding_ids + explanations + gap statements.
Adversarial (synthetic fixtures, labelled):
- prompt_injection_in_draft: draft contains "ignore previous... " — extraction treats as claim text only; schema rejects unexpected fields; finding explains quote context; no tool call triggered.
- fabricated_reference: finding references DB:id=999 -> EVIDENCE_GAP (not false positive); reference check fails; output flags gap.
- malformed_model_output: model returns extra fields / wrong category -> Pydantic rejects; output includes UNCERTAIN label; never promoted to SUPPORTED.
- contradictory_registry: registry BLOCKED + draft present -> finding CONTRADICTORY with both sources cited.
- source_mutation_attempt: proposal file modified during run -> read-only open prevents; or compare pre/post hash; failure if mutation detected.
- unsupported_conclusion: claim with DB=0 rated SUPPORTED -> test asserts failure; output must be UNSUPPORTED/EVIDENCE_GAP.
End-to-end (owner-confirmed inputs): proposal claim line → quoted substring + file ref → DB count (currently 0) → finding UNSUPPORTED with EVIDENCE_GAP (DB:evidence=0, DB:interactions=0...) + question for owner. Traceable; synthetic fixtures labelled; real result is gap, not fabricated accuracy.
Regression (existing OSS-AgentOS): `tests/test_contract.py` (3/3); L11 sandbox tests (13/13); SQLite health; `uv.lock` unchanged; no G1 rewrite.

=== PHASE E — IMPLEMENTATION PLAN ===
Module: `src/agentos/cli_auditor.py` (registration); `src/agentos/domain/auditor_finding.py` (Finding/EvidenceLink/Pydantic schemas); `src/agentos/core/auditor_service.py` (load/identify/compare/evaluate/format — read-only); reuse `db/repository.py` / `evidence_repo.py` read patterns.
Staged order (after owner approves this design):
1 Schema + domain model (Pydantic Finding); synthetic fixture tests (labelled SYNTHETIC).
2 Input loader (proposal/idea/hours/DB SELECT); identity/consistency checks; read-only enforcement.
3 Claim extractor (quote substrings, line refs); evidence matcher (DB SELECT); gap identification.
4 Finding builder + validation; output format; CLI entry.
5 Integration + adversarial tests; end-to-end with real inputs; regression checks.
6 Documentation update (if needed); not required for core.
Dependencies (none required; if semantic analysis later: owner approval + isolated analyst + validation layer — not now). External: none (SQLite local; no model provider configured; `act=OFF` preserved).
Limitations / block conditions: without owner-provided proposal text content (draft source confirmed but CONTENT not reproduced here per critic-only rule — quote extraction requires reading file at run time), auditor outputs only EVIDENCE_GAP / MISSING_SOURCE / CONTRADICTORY findings; semantic grading remains UNCERTAIN until either (a) evidence linked, or (b) model approved + validated — neither claimed here. L11 amendment scope preserved; no L12 / extractor / PR shepherd started.

=== VERIFICATION SUMMARY ===
Design verified against: real `cli_*.py` patterns; `evidence_repo.py` (read-only + validation pattern); `models.py` (Pydantic v2); `connection.py` / SQLite; `pyproject.toml` / `uv.lock`; `AGENTS.md` §4/§7/§12/§14; plan §2.7/§6.10; spec freeze doc; input-registration doc; L11 amendment; DB counts; registry; no synthetic accuracy claimed.
Not implemented: no source edited beyond this design doc; `cli_auditor.py` not created; DB untouched; proposal not reproduced.
Awaiting owner's approval of this architecture before Prompt 4 implementation begins.
