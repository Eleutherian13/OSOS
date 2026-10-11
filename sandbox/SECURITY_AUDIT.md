# Sandbox Adversarial Security Tests + Report (Prompt 4)
# Act: verified disabled (no .github/workflows; no act integration; no automatic install/execution).
# Tests use harmless payloads only; no destructive host/test against user's repo.

adversarial_tests (§B):
  - arbitrary_host_cmd: try inject via cmd arg / filename / config -> allowlist rejects (verified design; execution BLOCKED)
  - escape_work: write to /etc / $HOME / source repo outside /work -> ro base + container (designed; BLOCKED)
  - host_file_access: read /etc/shadow / docker.sock / ssh/ -> no host mounts (designed; BLOCKED)
  - network_reach: curl pypi / github / internal -> --network none (designed; BLOCKED)
  - secrets_read: env / ssh-agent / cloud creds -> none mounted (verified design)
  - resource_exceed: cpu/mem -> 2/4G + container limit (designed; BLOCKED)
  - bg_survive: sleep 300 -> pid namespace kill (designed; BLOCKED)
  - cmd_bypass: shell metacharacters / redirect / quote -> allowlist exact-match (verified design)
  - repo_modify_outside: touch source outside /work -> ro + disposable (designed; BLOCKED)
  - symlink_traverse: symlink /work -> /etc; attempt read -> blocked (designed; BLOCKED)
  - inject_filename_output_config: malicious filename / stdout / config -> treated untrusted; no execution (design)
  - upstream_write: attempt outbox/gh post -> Guard/Outbox authorization required separately; sandbox has no upstream write authority

repairs: none applied (no defects found at design level; runtime absence is the blocker, not a code defect to repair). Would rerun isolation tests against real runtime when available (not faked).

security_report_file: docs/LEVEL_11_SANDBOX_SECURITY_REPORT.md (created below)
act_default: DISABLED (preserved; no installation triggered)
