# Level 11 Sandbox — CONTROL PLANE ONLY (runtime BLOCKED)
# Trigger check (AGENTS.md §4): NOT satisfied — no COPILOT mode, no measured
# reproduction/testing bottleneck, Docker unavailable, G1=FAIL preserved.
# Source of truth: AGENTS.md > this file > design docs only (§1, §4, §11, §15).
# G1 status preserved FAIL; G1_OVERRIDE_AUTHORIZED preserved; not rewritten.

status: CONTROL_PLANE_ONLY
runtime_execution: BLOCKED (no container runtime; no host execution of untrusted code)
trigger_satisfied: FALSE
authorization: User-selected defer (prompt 0 answer = "Neither — defer")

safety_preserved:
  - G1 = FAIL (not rewritten to PASS)
  - G1_OVERRIDE_AUTHORIZED = preserved
  - Guard / Outbox / approval tokens / kill epoch / kill switch
  - Rolling 30-day budget (not replaced by calendar month)
  - No fabricated isolation / benchmark / pass claims

architecture (designed, not fully executed due to BLOCKED):
  Stage A Prefetch: allowed registries, lockfile/hash verify, controlled volume,
                    fail-closed on verification failure. No target-script execution
                    during unrestricted prefetch.
  Stage B Run: --network none (target); ro base FS; writable /work only;
               2 CPU / 4 GB / 30m max; no secrets; no host mounts;
               verified test_cmds allowlist only; bounded output; terminate on
               limit exceed; act replay disabled by default (untrusted workflow).
