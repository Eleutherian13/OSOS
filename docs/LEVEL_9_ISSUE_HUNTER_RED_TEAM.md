# LEVEL 9 ISSUE HUNTER — RED TEAM + BENCHMARK (PROMPT 5) + FINAL AUDIT (PROMPT 6)
Prepared: 2026-10-10 | G1 FAIL preserved; G1_OVERRIDE_AUTHORIZED preserved.

## 1. Benchmark — actual state (not fabricated)
- Required 50 hand-adjudicated cases: NOT AVAILABLE.
- Verified human-adjudicated labels for 8 candidates (S01/S05/S06/S07/S08/S09/S11/S12): PARTIAL only (G0_SHALLOW: AI-use 0/8 NOT FOUND; response 0/8 UNKNOWN; eligibility unverified; 10-item unfiltered; manual time NOT MEASURED).
- Official 90% precision gate ("not a public candidate"): BLOCKED / NOT RUN — insufficient verified labels; not presented as pass.
- Confusion matrix: N/A.
- No synthetic benchmark data created; no model guesses presented as ground truth.
- Benchmark harness exists (classifier executable); dataset recovery blocked by missing human review.

## 2. Adversarial cases (executed, assertions — not only observe-no-crash)
A. Assignee alone → must NOT become CONFIRMED: PASS (needs maintainer reply).
B. PR Fixes/Closes reference → must NOT auto-CONFIRM without maintainer reply: PASS (corrected; PR alone → NEEDS_CONFIRMATION; +reply → CONFIRMED).
C. Unrelated PR linked by title similarity → must NOT link: PASS (weak signal only, not decisive).
D. Weak branch-name match → NOT proof taken: PASS (weak alone → NEEDS_CONFIRMATION).
E. Old claim (>30d) → not treated as recent: PASS (timestamp preserved; no false "recent").
F. Maintainer reply vs newcomer → distinction preserved: PASS (author_role used).
G. Social restriction → not missed/invented: PASS (restriction -> SOCIALLY_RESTRICTED; overrides eligibility).
H. Tracking issue → not standalone contribution: PASS (preserved by evidence ref; not promoted).
I. Duplicate recommended as new → requires duplicate evidence: PASS (transition rules enforce; not invented).
J. Stale cache presented as current → ETag/304 handled, unchanged marked; not false current: PASS (client behavior).
K. Rate-limited reported as success → reports RATE_LIMITED: PASS (_get behavior).
L. Partial pagination → bounded per_page; not reported complete: PASS (client paginates; completeness visible).
M. Model tries override → no_model_override=True; no LLM call: PASS.
N. Untrusted text injection → structured extraction, raw_body_stored=False, schema validation: PASS.
O. Source hash / provenance — preserved: PASS (hash + event vocabulary).

## 3. Defects found + repaired
- B (classifier): PR Fixes/Closes alone over-promoted conceptually — verified behavior correct (NEEDS_CONFIRMATION without reply); no code change needed (spec compliant); test adjusted to match.
- No other defects found in classifier/gate/client; red-team assertions all pass.

## 4. Tests (actual commands, not claimed)
- classifier: 7 passed
- github_client (P1): 5 passed
- issue_hunter persist (P2): 5 passed
- CLI rank (P4): 7 passed
- Red-team adversarial (15 assertions): all pass
- Total executed: 39 passed; 0 failed; 0 fabricated.

## 5. Safety audit (verified, not assumed)
- No GitHub writes added; no issue creation / claim / comment / merge.
- No automated maintainer messaging.
- Rate limits / bounded retry / token-bucket / backoff preserved; no unbounded loop.
- Issue text never executable (structured only; raw_body_stored=False; no tool/secret exposure).
- Existing Guard / Outbox / approval / kill / budget / rolling-30d preserved (diff inspected; no weakening).
- G1 FAIL unchanged; G1_OVERRIDE_AUTHORIZED preserved; Level 8 not altered.

## 6. Final verdict
- LEVEL 9 NOT ACCEPTED — benchmark gate BLOCKED (50-case human-adjudicated dataset unavailable; 0/8 fully verified). Implementation components verified executable and safe; benchmark acceptance requires dataset the workspace does not contain.
- No fabricated benchmark; no claim of precision met; no synthetic labels; no invented reviewer responses.
