# LEVEL 4 PROMPTS 1-2 CONTRACT

## Previous levels verified from repo
BUILD_STATE: CURRENT 3. LEVEL_3_REPORT: ACCEPTED (freeze ready for 4). LEVEL_1/2 reports complete. Migrations V001-V003 present. DB unavailable for integration (documented, same Level 1/2 limitation). Level 4 was not implemented before.

## Registry (Prompt 1)
Canonical: registry/orgs/<slug>.yaml. Pydantic v2 (RegistryV21). Independent surfaces: proposal_text, proposal_estimate, code, understanding_aid, autonomous_agents, comms_text. Values: BLOCKED/ASSIST_ONLY/DISCLOSE/ALLOWED/UNKNOWN (no substitution). SourceRef per classification (id/url/excerpt/sha256/status=PENDING_BASELINE); hash validated 64-hex; PENDING_BASELINE visible, not monitored. Contact: channel explicit (empty/unknown rejected); DM false by default; quote + source_ref. human_confirmed false always initially; reconfirmation_needed + reason explicit.

## Provenance / hash lifecycle (Prompt 0/1)
Stable source ID + URL + excerpt required. SHA-256 when snapshot available; else status=PENDING_BASELINE (Level 5 baseline). No HTTP fetch; no LMM extraction; no watcher (Level 5). Source-text/hash representation: 64-char lowercase hex.

## Confirmation (Prompt 0/1)
Explicit human act only. Not inferred from file creation, YAML valid, DB sync, LLM output, URL existence. Registry kept human_confirmed=false; reconfirmation_needed=true.

## Policy engine (Prompt 2)
Two outputs: effective_mode (ceiling, derived only) and evaluate_policy(surface, context). Modes: OBSERVE/UNDERSTANDING_ONLY/ASSIST/COPILOT. Table deterministic (code BLOCKED -> UNDERSTANDING_ONLY; ASSIST_ONLY/DISCLOSE + autonomous BLOCKED/UNKNOWN -> ASSIST; ALLOWED + autonomous BLOCKED/UNKNOWN -> COPILOT; ALLOWED + autonomous ALLOWED -> COPILOT; unknown/unconfirmed/reconfirmation -> OBSERVE conservative). Fail-closed unconfirmed/reconfirmation -> restrict. Disclosure preserved; unrelated surfaces never escalated; AI drafts / human sends preserved.

## Database projection (contract documented, not fully built)
YAML canonical; PostgreSQL projection when needed; sync explicit; stale projection not silently used; additive migrations (V004 future); events via existing event_store.

## Contact / engagement (contract)
Unknown channel -> not ENGAGED; DM not welcome unless explicit; missing != permission; source/policy change -> reconfirmation possible; unconfirmed does not grant capabilities.

## Tests (delivered)
tests/unit/test_level4_policy.py: 13 pass. All enum values, invalid enums, missing fields, slug, URLs, hashes, unknown contact, DM default, confirmation, reconfirmation, derived-mode, disclosure, provenance — pass. No DB/network required.

## Lint / type
ruff / mypy: schema/engine clean (minor ruff formatting notes fixed by conventions; no logic errors). No secrets exposed.

## Exclusions respected (Prompt 0/9/10)
No watcher, HTTP fetch, LLM extraction, GitHub, Guard, Outbox, approval tokens, ranking, RAG, workers, dashboard, LLM execution.

## Unresolved ambiguities (documented, not hidden)
- AUTONOMOUS_AGENTS ALLOWED + code ASSIST_ONLY/DISCLOSE: spec silent; conservative ASSIST/restricted documented.
- DISCLOSE + ALLOWED + disclosure_required=true -> ALLOW_WITH_DISCLOSURE (preserved).
- Source-change reconfirmation: manual (reconfirmation_needed explicit); not auto-derived from URL timestamp (watcher deferred to Level 5).

## Security risks
Confirmation fraud prevented (not automated). Hash not proof of policy correctness (only snapshot integrity). Unknown = UNKNOWN not ALLOWED. Effective mode not independently editable. DB projection divergence observable.

## Implementation order executed per spec
Prompt 0 recon (inspection only, no edits) -> Prompt 1 schema/validation/registry/tests -> Prompt 2 engine/evaluator/tests -> stop (Prompt 0 exclusions + Prompt 2 stop instruction). Defer: DB projection V004, CLI sync, event emission, engagement enforcement, full integration.
