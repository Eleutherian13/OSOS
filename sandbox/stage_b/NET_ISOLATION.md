# Stage B — Network isolation (design; execution BLOCKED)
# Requirement (§C): no network access; enforce at runtime/OS layer (not env vars / app convention).
# Tests intended: reach public internet / pypi / git hosts / internal endpoints -> must fail.
# Actual: not executable — no container; no --network none mechanism available.
# No proxy inherited; no false claim of isolation.

enforcement_layer: container --network none / namespace isolation (absent)
actual_state: BLOCKED
verified_reach_attempt: NOT PERFORMED (would require either container or intentional host breach — prohibited by §11)
proxy_bypass_risk: not applicable (no container -> no false "isolated" claim)
