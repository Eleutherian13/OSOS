# Stage A — Prefetch (control-plane design only; not executed with untrusted code)
# Network restricted to allowlisted package registries.
# Resolve via existing package manager; verify lockfile + hashes; fail closed.

allowed_registries:
  - https://pypi.org/simple/ (project package manager, lockfile verified)
  - project-local /work/deps (controlled volume)

verification:
  lockfile: uv.lock / poetry.lock / pip-tools (existing)
  hashes: sha256 of fetched artifacts against lockfile entry
  failure_mode: FAIL_CLOSED (stop; do not proceed to Stage B)

controlled_volume: sandbox/stage_a/deps/
no_target_script_execution_during_prefetch: TRUE
