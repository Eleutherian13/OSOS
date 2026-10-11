# Stage B — Self-tests (design; safe payloads only; no real credentials)
# Per §G: attempt network access, write outside /work, read host mounts, access secrets, spawn persistent bg, exceed CPU/memory, exceed deadline, escape command restriction, excessive output.
# Each uses harmless test payload; none exposes credentials.
# Actual run: BLOCKED (no container) — tests defined, not falsely reported as passing.

tests_design:
  - net_reach_public: curl / ping to 1.1.1.1 / pypi.org -> must fail (network namespace blocked)
  - write_outside_work: touch /etc/test / $HOME/test -> must fail (ro base + no host mounts)
  - read_host_file: cat /etc/passwd / host-mounted secret -> must fail
  - secrets_env: env | grep SECRET / ssh-agent -> empty (no secrets mounted)
  - bg_spawn: sleep 300 & -> must terminate with parent (pid namespace / kill)
  - cpu_exceed: stress / cpu-bound loop -> must terminate at 2-core limit
  - mem_exceed: memory alloc loop -> must terminate at 4G
  - deadline_exceed: long-running task -> must terminate at 30m (container kill / timeout)
  - cmd_escape: attempt `echo ok; bash -c 'id'` via allowlist -> rejected (only exact commands)
  - output_excess: massive stdout -> truncated / terminated per policy
  - symlink_escape: symlink /work/escape -> /etc; attempt read -> blocked

harmless_payload_confirmed: TRUE
real_credentials_exposed: FALSE
actual_execution: BLOCKED (correct — not falsely reported pass)
