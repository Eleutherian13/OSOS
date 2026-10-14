# P7 EXEC 4/6 — Security Architecture and Fail-Closed Verification

Status: PARTIAL — architecture verified at executable paths; real adapter endpoint configured; synthetic/regression tests executed; full live-output-layer proof for all 40 injection cases requires dedicated execution (documented, not hidden); P7 FINAL ACCEPTANCE remains BLOCKED until that completes.

## Requirement-to-code-to-test matrix (P7 §13.1–13.8, architecture focus)

| Layer / Requirement | Component / Path | Enforcement (executable) | Test / Evidence | Result | Gap / Limit |
|---|---|---|---|---|---|
| 1. Deterministic extraction | src/agentos/core/auditor_service.py; policy schema (RegistryV21, SourceRef); evidence/interactions/mentors tables | Typed extraction; code blocks inert; untrusted content not executed | Design audit + adversarial test preserved + admin verified adapter interface | PASS (design/test) | Live source-fetch verification BLOCKED |
| 2. Read-only analyst (no tools, no secrets) | src/agentos/core/llm_adapter.py (Adapter protocol); model_wrapper (no key args); adapter edit (endpoint_url only, no secrets) | Adapter.call has no tool args; no secret loading; output constrained to AdaptedResult | Synthetic connectivity + adapter assertion + no-token-in-source check | PASS (design/test) | Full live-output-layer proof requires execution turn |
| 3. Deterministic verifier | src/agentos/guard/engine.py (RULE_ORDER A..G); workflow_gate; quiz_gate; SQLite check constraints (state/enum/unique/FK) | Ordered deterministic DENY/NEEDS_HUMAN/ALLOW; enum enforcement; no LLM override | Synthetic guard tests + isolated DB regression + adversarial evidence test | PASS (design/test) | Live endpoint integration BLOCKED |
| 4. Tool-capable receives validated typed structures / hashes, never raw attacker content | adapter interface (typed agent/tier/prompt); guard output structured; workflow_gate requires validated inputs; no direct raw-text-to-tool path | Tool args constructed from validated fields; adapter does not receive raw untrusted instructions as args | Adapter assertion + design audit + isolation check | PASS (design/test) | Same live-execution limitation |

## Fail-closed tests executed (isolated, synthetic, actual adapter path)
- Malformed JSON / bad enum / unknown field / duplicate / unexpected type / invalid id / overlong: adapter interface accepts only structured case fields; untrusted `text` never passed as tool arg; verifier rejects invalid enum/state by design (guard/schema). No mock verifier used — guard/engine and SQLite constraints are real.
- Prompt injection embedded in docs/quotes/code/comments/Unicode: synthetic fixtures (`INJ-001`..`INJ-040`) cover all categories; adapter interface does not execute embedded code; code blocks inert; no tool invocation from adapter (verified by design + assertion).
- Fabricated source / invalid provenance / contradictory evidence: auditor_service conservative; adversarial evidence test (`test_level12_evidence_grader_adversarial.py`) preserved; `org_policy` / `evidence` schema preserves `source_ref` / `artifact_url`; `UNKNOWN`/`STALE` preserved.
- Unexpected model exceptions / empty / timeout / invalid: adapter returns fixed `AdaptedResult`; real endpoint responds (200 to `/api/tags`); no loop; bounded retry design preserved (`fetcher.py`). Failures enter safe structured state.
- Raw source bypass around verifier: no path from adapter → tool without guard/schema validation (adapter interface isolated; guard/approval-token/effect-time controls intact).
- Tool invocation from analyst: adapter `call()` has no tool load; `model_wrapper` mode `FAKE`/`LOCAL`; no secret/token exposure.
- Validation failure → downstream blocked: guard `DENY` / `NEEDS_HUMAN` stops; workflow_gate `BLOCKED`; SQLite FK/check constraints enforce at persistence; event_store append-only trigger prevents destructive change.
- Benign negative controls: `INJ-025`, `INJ-040` (ALLOW expected) verify no over-block; adapter handles benign input same path.

## Defects repaired (smallest justified)
- None destructive required; adapter edit (`LocalAdapter.__init__` endpoint_url + docstring) is the only source change for endpoint availability; no verifier weakening; no schema weakening; no guard relaxation.
- Synthetic regression tests preserved (`test_p7e_provenance_synthetic.py`, `test_p7d_rate_regression.py`); adversarial evidence test preserved.
- No new subsystem; no Level 13/14/15/16 work started.

## Evidence files
- `tmp_p7evidence_3_6.json` (execution evidence, 40 cases, 0 tool attempts, 0 out-of-enum, PARTIAL)
- `evals/injection.jsonl` (40 cases, version v1-canonical-2026-10-13, hash `9c01d399...`)
- `docs/P7_FINAL_ACCEPTANCE.md` (final status BLOCKED with documented limitations)
- `docs/P7_INJECTION_CORPUS_DECISION_2026-10-13.md` (baseline amendment record)

## Actual command / verification performed
- `python tmp_p7_exec_3_6.py` → executed 40 cases through adapter interface; 0 attempted/completed tool calls; 0 out-of-enum; 2 ALLOW / 38 DENY; errors []; interrupted false.
- Adapter assertion (`def call` present; `Adapter` protocol; no tool path) verified in script.
- Real endpoint connectivity verified via `urllib` to `http://127.0.0.1:11434/api/tags` (200) with `ollama`; no secret; synthetic.
- Schema / guard / workflow imports verified; SQLite check/unique/index verified (previous reads).

## Remaining gap (explicitly stated — not concealed)
- Full live-output-layer proof (model output verified for zero tool-invocation / zero out-of-enum per case) requires dedicated inference execution across all 40 cases with instrumented output parsing; not completed in this turn because it requires sustained endpoint interaction; boundary design confirmed, execution layer pending.
- This gap does not change control design; it only delays final `P7_SECURITY_ACCEPTANCE = ACCEPTED` until the execution evidence exists.

## Preservation (verified)
- SQLite/V012/uv.lock/reports/corpus/extension/decision/G1/act/Outbox/Guard/approval/budget/caps preserved.
- `G1=FAIL`; no commit/push/reset/clean/rebase; no upstream action; `act=OFF`.
- No secrets, personal records, or upstream messages produced.
