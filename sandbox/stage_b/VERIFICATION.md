# Stage B — Output, termination, and isolation verification (Prompt 2)
# Bounded stdout/stderr capture; termination on timeout / memory / failure / cancellation; explicit outcomes (not false success).
# Verification of enforced restrictions (per acceptance): must show actual runtime behavior.

bounded_capture: designed (max output size; truncate / terminate policy documented)
termination_reasons: timeout / mem_exhaust / runtime_failure / user_cancel -> all explicit (not masked as success)
descendant_termination: container kill / pid namespace (intended; not present — reported)
actual_verification_status: BLOCKED (no runtime = no behavior to verify; not invented)
unverified_properties: network isolation (no container to test); filesystem isolation (no container); resource limits (no container); cmd escape (no execution); bg termination (no execution)
correct_reporting: BLOCKED — not falsified as PASS
