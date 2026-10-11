# Sandbox CLI / Orchestration — control-plane design (Prompt 3; execution BLOCKED)
# Reuses existing conventions (cli_path/cli_report/evidence-ledger) — no new framework.

lifecycle (deterministic, per §B):
  1 resolve_path_rev(lambda payload path + git rev) -> verify source revision
  2 verify_sandbox_authorized(mode) -> reject if not authorized / mode unsupported
  3 resolve_approved_commands(test_cmds yaml) -> reject if unverified / unlisted
  4 prefetch(stage_a) -> uv sync / lockfile verify; FAIL_CLOSED if bad
  5 integrity_check -> record hash outcomes; fail closed if mismatch
  6 prepare_workspace(isolated /work) -> disposable; ro base
  7 enforce_isolation(runtime) -> BLOCKED (no container)
  8 execute_approved(cmd) -> BLOCKED
  9 capture_logs_exit_duration_termination -> bounded; explicit reasons
  10 store_report(evidence_ledger + path + task link) -> traceable; not synthetic
  11 cleanup(disposable) -> remove /work artifacts

failure_handling_separate (§E): prefetch | integrity | runtime_avail | isolation | invalid_cmd | timeout | resource_limit | test_fail | success -> never convert infra failure to pass.

cli_integration (§C):
  - inspect_sandbox_capability (mode + runtime check)
  - validate_test_cmds (verify_cmds.yaml format + allowed executables)
  - prefetch_deps (stage_a; requires rev + mode auth)
  - run_isolated (requires all above + functioning runtime; rejects otherwise)
  - inspect_run (report from evidence)

rejection_criteria (§C): no verified source rev -> reject; no approved cmd list -> reject; no functioning isolation runtime -> reject (BLOCKED; not substituted).

evidence (§D): repo + rev, manifest/lockfile hashes, cmd list, runtime config, start/end, exit codes, termination reason, integrity pass/fail, isolation pass/fail, cmd pass/fail, output refs / truncation, limitations, synthetic-vs-real flag. Not a mentor-validation event; not readiness-complete by command run.

actual_state: control plane designed; execution BLOCKED (runtime unavailable; G1 FAIL preserved; container absent); CLI not fully wired (would require working runtime first — correct ordering).
