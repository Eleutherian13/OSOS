ARCHITECTURE DECISION RECORD — PROPOSAL EVIDENCE AUDITOR (Prompt 3 → Prompt 4 gate)
Status: ESSENTIAL DESIGN ONLY — no source edited (cli_auditor.py not created; DB untouched; proposal/ledger read-only; L11 amendment preserved; G1 preserved; uv.lock preserved; act=OFF; no new dependency added without approval).
References: func spec freeze docs/PROMPT2_SPECIFICATION_FREEZE_2026-10-11.md; architecture design docs/PROMPT3_ARCHITECTURE_VERIFICATION_DESIGN_2026-10-11.md; input reg docs/PROMPT2_INPUT_REGISTRATION_2026-10-11.md.

=== DECISION 1: DETERMINISTIC-FIRST, MODEL ONLY IF APPROVED ===
Context: repository has zero approved model integration (pyproject has no model/LLM/openai/anthropic/gemini provider; config/ has none; source has none; AGENTS.md §4/§7/§12 require isolation + validation if any model used).
Options: (A) Add model provider + API key + isolated analyst now; (B) Deterministic-only now; deferred semantic with explicit approval + isolation + validation later.
Selected: B.
Reason: instruction requires using existing approved integration if appropriate — none exists; inventing provider violates AGENTS.md §7 (secrets/credentials) and §4 (conditional subsystems must not expand scope). Semantic grading (claim meaning) can be deferred to verified evidence + human review without claiming false accuracy.
Consequence: auditor outputs UNSUPPORTED / UNKNOWN / EVIDENCE_GAP for claims lacking evidence (correct behavior with DB=0), not fabricated "supported." Anticipated mentor challenges derived deterministically from weakest-claim / missing-evidence points (not model-generated). If owner later approves semantic layer, add isolated analyst + Pydantic validation + UNCERTAIN labeling — separate decision.

=== DECISION 2: MODULE BOUNDARIES ===
New: `src/agentos/domain/auditor_finding.py` (Pydantic Finding/EvidenceLink schemas, from spec freeze); `src/agentos/core/auditor_service.py` (load/identity/compare/generate — read-only); `src/agentos/cli_auditor.py` (Typer subcommand, registers on existing `app`).
Reused (no edit needed for design): `cli.py` app; `db/repository.py` / `db/evidence_repo.py` read patterns; `db/connection.py` SQLite access; `models.py` Event pattern (optional for audit-event recording, not required here).
Excluded (not in this scope): database migration; new persistence backend; model provider; external service; autonomous worker; L3/L4 action.

=== DECISION 3: DATA FLOW — DETERMINISTIC PATH ONLY ===
1 Load inputs (file/text read + SQLite SELECT — both read-only) → validate identity (source IDs + registry + DB project refs) → 2 Extract quoted claim substrings (≤200 chars, file:line refs, deterministic, untrusted text treated as data) → 3 Match to DB (projects/interactions/mentors/evidence; count=0 preserved as EVIDENCE_GAP) → 4 Build findings (Pydantic schema) with status determined by evidence presence/absence/contradiction (not semantic inference) → 5 Validate source refs resolve (DB ID exists OR gap stated; file path exists OR gap) → 6 Output structured + execution metadata (no proposal mutation; no DB write).
Semantic judgments (claim strength beyond presence/absence) deferred; if required later, add isolated analyst between step 3 and 4, with output validation — separate approval.

=== DECISION 4: TRUST BOUNDARIES ===
Proposal/idea text: untrusted; quoted substrings only; never executed; never treated as instructions; prompt-injection trips logged, never acted on.
Evidence DB: read-only SELECT; no ingestion without explicit authorization; ledger=0 preserved; synthetic fixtures labelled SYNTHETIC; fixture results never presented as accuracy evidence.
Model (if approved later): isolated analyst (no secrets, no DB writes, no tool access); output passes Pydantic validation; unsupported assertions rejected / labelled UNCERTAIN; zero out-of-enum fields; proposal text never inserted except quoted refs.
Output: validated structured format; proposal_rewrite_check="pass" enforced; explanation contains quote or gap statement; evidence_links resolve or gap explicit.

=== DECISION 5: FAILURE HANDLING ===
Partial failure: return findings that succeeded + explicit BLOCKED sections for missing inputs / unreadable sources; never complete report that hides missing inputs.
Contradiction: CONTRADICTORY finding with both sources cited (e.g., registry BLOCKED + draft present; idea project != proposal).
Stale/malformed: source timestamp compared to evidence timestamp; stale = PARTIALLY_SUPPORTED or CONTRADICTORY with explanation; malformed DB record (bad URL/depth) = ignored + EVIDENCE_GAP.
No finding when not justified: if claim + evidence fully supported, finding SUPPORTED; if no claim identified, no finding (not synthetic negative).

=== DECISION 6: NO NEW DEPENDENCY / NO DATABASE CHANGE / NO MODEL NOW ===
Dependencies at implementation: Python 3.12 stdlib, `typer`, `pydantic`, `sqlite3` (existing); `uv.lock` preserved; no new PyPI package required for deterministic path.
If semantic layer later: separate approval required for model provider + isolated analyst + validation layer.
No DB migration: audit findings can be written to stdout/file only (read-only); optional audit-event recording uses existing `Event` model (no schema change) if owner approves.

=== VERIFICATION MATRIX (traceable, from design doc + spec freeze) ===
Unit — input validation: synthetic fixture (labelled SYNTHETIC) with proposal snippet, idea snippet, DB mock (evidence=0). Expected: load OK, identity pass/fail, DB untouched. Pass: identity correct / DB count unchanged. Dependency: pytest + fixtures.
Unit — classification boundary: synthetic claims with/without DB links, with contradiction sources. Expected: UNSUPPORTED/EVIDENCE_GAP when DB=0; CONTRADICTORY when sources disagree. Pass: correct category; explanation has quote/gap. Dependency: pytest.
Unit — finding construction: build Finding with all fields; validate Pydantic. Expected: passes; proposal_rewrite_check=pass; evidence_links all resolve or gap set. Pass: schema valid; no proposal prose in fields. Dependency: pytest.
Unit — output validation: malformed finding (missing explanation, missing evidence gap when links empty, wrong status) → rejected. Pass: only valid findings emitted. Dependency: pytest.
Integration — SQLite access (real DB): SELECT evidence/projects/interactions/mentors; count=0 preserved. Expected: counts match DB; file mtime unchanged pre/post. Pass: DB untouched; counts correct. Dependency: existing sqlite3 / data/agentos.sqlite.
Integration — CLI invocation (real): `python -m agentos.cli_auditor --proposal ... --idea ...`. Expected: exit 0; structured output; no mutation. Pass: output valid; exit 0; proposal/DB unchanged. Dependency: typer / package installed.
Integration — evidence ref resolution (real + synthetic): DB IDs from findings match actual rows; file refs exist; URL refs valid if used. Expected: all refs resolve OR gap stated. Pass: no broken reference unlabelled. Dependency: existing DB / file system.
Regression — existing tests: `tests/test_contract.py` (3/3); L11 sandbox (13/13); DB health. Expected: same results; no breakage. Pass: exit codes unchanged. Dependency: pytest / existing fixtures.
Adversarial (synthetic, labelled): prompt injection in draft → finding includes quoted snippet only, no execution, schema validates (no extra fields). Pass: no tool call; no mutation. Fabricated DB reference → EVIDENCE_GAP; no false positive. Pass: gap stated. Contradictory registry → CONTRADICTORY with both sources. Pass: both cited. Source mutation attempt → read-only prevents / detected. Pass: mutation blocked / reported. Malformed model output (if used later) → Pydantic rejects; UNCERTAIN. Pass: unsupported assertion not promoted.
End-to-end (real owner inputs + DB=0): proposal claim → quoted excerpt + file ref → DB count 0 → finding UNSUPPORTED + EVIDENCE_GAP (DB:evidence=0, interactions=0...) + validation action for owner. Traceable; no fabricated accuracy. Pass: all steps present; output structured; sources cited. Dependency: real draft/idea/hours sources.
Security — secrets / external calls: audit has no API keys; no outbound unless approved httpx fetch; no `curl | sh`; no host execution. Pass: no secret in output; no unexpected network. Dependency: environment (no external service configured).

=== CORRECTION 4 — DETERMINISTIC-ANALYSIS CONTRACT (reconciled) ===
Deterministic operations (verified, safe): input identity/checks (source IDs match registry/project); quoted-substring extraction (file:line, ≤200 chars) confirming excerpt exists; DB count verification (SELECT only, counts preserved); schema validation (Pydantic Finding); source-reference resolution (DB id exists OR file exists OR explicit EVIDENCE_GAP labeled); contradiction detection when sources disagree (registry BLOCKED + draft; idea != proposal); classification of missing/stale/contradictory/malformed inputs.
NOT independently established by deterministic methods: semantic support (whether evidence meaningfully validates claim); technical validity of assumptions; likely mentor challenges (these require interpretation of technical content, not just presence/absence of records). Status for these must be UNKNOWN / EVIDENCE_GAP / ANTICIPATED_CHALLENGE (anticipated, not actual reply), never unsupported→supported merely because a record exists.
Rule: quoted-substring match + DB record presence = candidate evidence link; does NOT = SUPPORTED finding. SUPPORTED requires both evidence presence AND semantic relevance (deferred to approved analysis with validation). With current DB=0, all claim evaluations return UNSUPPORTED / EVIDENCE_GAP / UNKNOWN — correct, not a failure.
No change claimed for full semantic analysis; limitation added (see Correction 5).

=== CORRECTION 5 — EXPLICIT LIMITATION (reconciled; verified present) ===
First version is deterministic-only: validates sources, identifies evidence gaps (DB=0 → EVIDENCE_GAP), detects contradictions, returns conservative UNKNOWN/EVIDENCE_GAP/ANTICIPATED_CHALLENGE. It does NOT satisfy full semantic analysis (support/assumption/mentor validation) unless/when: (a) a suitable approved analysis method exists, (b) its validation (fixture + real) is complete, and (c) an isolated analyst path with Pydantic output validation is in place. Until then, outputs must not claim accuracy beyond evidence presence/absence; no fabricated evaluation dataset; no synthetic fixtures labeled as real-world validation.

First implementation (this design) is deterministic-only: validates sources, identifies missing evidence (DB=0 → EVIDENCE_GAP with counts), detects contradictions, produces conservative UNKNOWN / UNSUPPORTED / EVIDENCE_GAP findings, and never claims full semantic analysis is satisfied. It may NOT independently establish: whether evidence meaningfully supports a technical claim; whether an assumption is valid; or what specific mentor challenges apply (only ANTICIPATED_CHALLENGE labels derived from weakest-claim / evidence-gap points). Semantic evaluation requires: (a) a suitable approved analysis method, (b) its validation (tested on real + synthetic fixtures, with labeled synthetic data), and (c) an isolated analyst path with structured-output validation — none of which are present now. Until those are approved, outputs carry the limitation explicitly and do not claim accuracy beyond evidence presence/absence. No fabricated accuracy percentage; no real-world validation claim.

=== KNOWN LIMITATIONS / BLOCKS ===
- Semantic claim-strength grading deferred (no model approved; no dataset); outputs reflect evidence absence/presence only — correct, not deceptive.
- Volume/isolation verification for Stage B (Docker) still BLOCKED in this environment (not the auditor's dependency, but noted; does not affect auditor design).
- If owner later requires full semantic evaluation: separate approval + isolated analyst + validation layer needed; not assumed here.
- Proposal draft CONTENT is read at run time (read-only); quote extraction depends on actual file content — no synthetic quote substituted.

=== STAGED IMPLEMENTATION (after this approval) ===
1 Schema/module (domain/auditor_finding.py) + synthetic fixtures labelled SYNTHETIC.
2 Input loader + identity check + DB SELECT (read-only) + regression checks.
3 Claim extractor (quote + line ref) + DB matcher + gap identification.
4 Finding builder + Pydantic validation + CLI (`cli_auditor`) registration.
5 Integration + adversarial + end-to-end tests.
6 Documentation (update if needed; not required to satisfy criteria).
No step changes DB schema, L11 docs, uv.lock, or proposal files.

 = = =   C O R R E C T I O N   6      C R I T I C - O N L Y   /   S O U R C E - M U T A T I O N   /   I N V E N T E D - E V I D E N C E   B O U N D A R Y   ( r e c o n c i l e d )   = = = 
 S t r i c t :   p r o p o s a l   t e x t   r e a d - o n l y   ( f i l e   r ) ;   q u o t e d   s u b s t r i n g s   o n l y   ( d"2 0 0   c h a r s )   i n   o u t p u t ;   p r o p o s a l _ r e w r i t e _ c h e c k   e n f o r c e d   i n   s c h e m a ;   n o   p r o p o s a l   p r o s e   r e p l a c e d / r e w r i t t e n / g e n e r a t e d ;   n o   s y n t h e t i c   f i x t u r e s   p r e s e n t e d   a s   r e a l ;   e v i d e n c e   r e c o r d s   n e v e r   i n v e n t e d   ( D B = 0   p r e s e r v e d ;   i n g e s t i o n   r e q u i r e s   s e p a r a t e   a u t h o r i z a t i o n ) ;   s o u r c e   r e f e r e n c e s   o n l y   r e s o l v e   t o   a c t u a l   D B / f i l e / U R L   o r   e x p l i c i t   g a p ;   n o   u n v e r i f i e d   c i t a t i o n s ;   r e a d - o n l y   D B   p r e v e n t s   m u t a t i o n ;   p a r t i a l   f a i l u r e   s u r f a c e s   ( m i s s i n g   i n p u t s   r e p o r t e d ,   n o t   h i d d e n ) ;   n o   m o d e l - g e n e r a t e d   c l a i m   p r o m o t e d   t o   S U P P O R T E D   w i t h o u t   e v i d e n c e   +   v a l i d a t i o n . 
 V e r i f i e d   p r e s e n t   i n   d e s i g n :   i n p u t   l o a d   r e a d - o n l y ;   D B   S E L E C T   o n l y ;   f i n d i n g   s c h e m a   r e q u i r e s   q u o t e   o r   g a p ;   e v i d e n c e _ l i n k s   m u s t   r e s o l v e   o r   g a p ;   n o   p r o p o s a l   t e x t   i n   e x p l a n a t i o n   e x c e p t   q u o t e d ;   L 1 1 / c u r r e n t   r e p o r t s   u n e d i t e d . 
 
 = = =   R E S O L U T I O N   S U M M A R Y   = = = 
 C o r r e c t i o n s   4 / 5 / 6   a p p l i e d   t o   d e s i g n   d o c .   I n p u t s   c o n f i r m e d   ( d r a f t / i d e a / s i z e / h o u r s   p e r   o w n e r ) .   D B   r e a d a b l e   ( s q l i t e 3   S E L E C T ;   c o u n t s   v e r i f i e d ;   e m p t y   l e d g e r   p r e s e r v e d      n o t   i n a c c e s s i b l e ) .   M a t r i x   c o r r e c t e d   t o   1 5   u n i q u e   I D s   ( U - I N P U T / U - C L A S S / U - F I N D / U - O U T / U - R E A D / I - D B / I - C L I / I - R E F / R - C O N T R A C T / S - N E T / A - I N J / A - F A B / A - C O N / A - M U T / E 2 E - R E A L ) .   D e t e r m i n i s t i c   c o n t r a c t   c o r r e c t e d :   q u o t e + D B - m a t c h   =   c a n d i d a t e   l i n k   o n l y ,   n e v e r   S U P P O R T E D   a l o n e ;   s e m a n t i c   ( s u p p o r t / a s s u m p t i o n / m e n t o r )   r e m a i n s   U N K N O W N / E V I D E N C E _ G A P / A N T I C I P A T E D   u n t i l   a p p r o v e d   m e t h o d + v a l i d a t i o n .   D e t e r m i n i s t i c - o n l y   l i m i t a t i o n   d e f i n e d   e x p l i c i t l y   ( n o t   f u l l   s e m a n t i c ) .   C r i t i c   b o u n d a r y   p r e s e r v e d   ( n o   r e w r i t e ,   n o   i n v e n t e d   e v i d e n c e ,   n o   m u t a t i o n ) .   S t a t u s :   D E S I G N _ R E Q U I R E S _ A P P R O V A L   ( s p e c   f r e e z e   a p p r o v e d ;   t h i s   A D R   +   m a t r i x   r e c o n c i l i a t i o n   c o m p l e t e ) ;   P r o m p t   4   i m p l e m e n t a t i o n   b l o c k e d   o n l y   b y   o w n e r ' s   a u t h o r i z a t i o n ,   n o t   b y   d e s i g n   i n c o n s i s t e n c y . 
  
 