# Stage B — Run (design only; runtime BLOCKED — no container, no host execution)
# Isolation requirements (spec §3, §4, §11):
#   --network none; ro base filesystem; writable /work only;
#   2 CPU / 4 GB / 30 min max; no secrets; no host mounts;
#   verified test_cmds allowlist; bounded output; terminate on exceed;
#   act replay OFF by default (workflow files untrusted).

isolation_mechanism_required: container_run (docker/podman) OR OS-level (cgroups/ns/jail)
available_in_environment: NONE (docker not present; no container runtime verified)
execution_on_host_of_untrusted_code: PROHIBITED by AGENTS.md §4 / §11

run_constraints:
  network: disabled
  base_fs: read-only
  writable: /work (sandbox/work/)
  cpu: 2
  memory: 4GB
  timeout: 30m
  secrets: none mounted / none in env
  host_mounts: none

allowlist_path: sandbox/test_cmds/verified_cmds.yaml
act_replay_default: DISABLED
collection: bounded stdout/stderr + exit code; terminate if exceeds limits
