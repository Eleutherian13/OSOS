# LEVEL 11 — SECURITY AUDIT REPORT

**Date:** 2026-10-11  
**Audit Target:** Level 11 Sandbox (Stage A Prefetch, Stage B Isolation, Orchestrator, CLI, Command Allowlist, Artifact Export)  
**Overall Security Status:** Control-Plane Boundaries `PASS` | Live Runtime Isolation `BLOCKED` (Host Daemon Unavailable)

---

## 1. Security Boundary Verification Matrix

Per `AGENTS.md` §7 and §11 (*"Do not mark a security boundary PASS without evidence that the real runtime enforced it"*):

| Security Boundary | Control Specification | Control-Plane Verification | Live Runtime Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Network Isolation** | `--network none` | Container command builder tested | Host container daemon missing | `UNVERIFIED (BLOCKED)` |
| **Read-Only Root FS** | `--read-only` | Root FS flags verified in orchestrator | Host container daemon missing | `UNVERIFIED (BLOCKED)` |
| **Workspace Confinement** | `--tmpfs /work:rw,exec,nosuid,size=4g` | Isolated tmpfs mount verified in cmd | Host container daemon missing | `UNVERIFIED (BLOCKED)` |
| **Resource Limits (CPU/RAM)** | `--cpus 2 --memory 4g` | Cgroup flags verified in orchestrator | Host container daemon missing | `UNVERIFIED (BLOCKED)` |
| **Timeout Enforcement** | Subprocess timeout (1800s default) | Tested via `test_timeout_enforcement` | Subprocess kill verified | **`VERIFIED (PASS)`** |
| **Command Restrictions** | Allowlist (`verified_cmds.yaml`) + regex check | Tested via `test_denied_command_*` | Rejects unlisted & injection | **`VERIFIED (PASS)`** |
| **Artifact Export Safety** | Traversal checks (`..`, absolute paths) | Tested via `test_failed_artifact_export_traversal` | Blocked directory escapes | **`VERIFIED (PASS)`** |
| **Fail-Closed Missing Runtime** | Strictly no host fallback | Tested via `test_missing_runtime_fails_closed` | Blocks with code 125 | **`VERIFIED (PASS)`** |
| **Dependency Integrity Gate** | Lockfile SHA-256 + PyPI allowlist | Tested via `verify_integrity.py` | Cryptographic check enforced | **`VERIFIED (PASS)`** |
| **Guard / Outbox Invariants** | ActionClass L1 only; L3/L4 rejected | Tested via `test_approval_bypass_attempt` | Outbox bypass blocked | **`VERIFIED (PASS)`** |
| **Kill-Switch Enforcement** | Preflight check against kill state | Tested via `test_kill_switch_active` | Immediate halt on STOP | **`VERIFIED (PASS)`** |
| **`act` Default State** | `act_enabled = False` | Hardcoded disabled in orchestrator | Untrusted workflows blocked | **`VERIFIED (PASS)`** |

---

## 2. Security Findings & Defect Log

### Finding 1: Host Container Runtime Daemon Missing
- **Severity:** HIGH
- **Component:** Stage B Live Execution Runtime
- **Description:** Docker Desktop and Podman are not installed or operational on the Windows 11 host. Background installer execution is blocked by Windows UAC elevation requirements (see [LEVEL_11_RUNTIME_INSTALL_REPORT.md](file:///c:/users/manas/OneDrive/Desktop/openOs/docs/LEVEL_11_RUNTIME_INSTALL_REPORT.md)).
- **Impact:** Live container execution cannot run.
- **Fail-Closed Remediation:** The orchestrator enforces strict fail-closed behavior (`RUNTIME_UNAVAILABLE`, exit code 125) and explicitly refuses to execute untrusted code on the Windows host.
- **Resolution Status:** `REMEDIATED (FAIL-CLOSED)`. Live execution remains `BLOCKED` pending owner interactive UAC installation.

### Finding 2: Potential Shell Metacharacter Injection in Command Arguments
- **Severity:** MEDIUM
- **Component:** `src/agentos/sandbox_orchestrator.py`
- **Description:** If raw command strings containing `;`, `&`, `|`, or backticks were passed directly to shell wrappers, command chaining could occur.
- **Remediation:** Added strict regex validation `re.search(r"[;&|`$<>]", command_str)` and strict exact-string allowlist matching against `sandbox/test_cmds/verified_cmds.yaml`.
- **Test Evidence:** Verified in `test_denied_command_shell_injection` (exits 127 `COMMAND_DENIED`).
- **Resolution Status:** `RESOLVED`.

### Finding 3: Path Traversal Vulnerability in Artifact Export
- **Severity:** MEDIUM
- **Component:** `validate_artifact_export()`
- **Description:** Untrusted container jobs could attempt to export artifacts using relative traversal paths (`../../secret.txt`) to overwrite host files outside the export target.
- **Remediation:** Enforced strict path normalization and `relative_to()` boundary checks on both source workspace and destination directory.
- **Test Evidence:** Verified in `test_failed_artifact_export_traversal` (exits 1 `EXPORT_FAILED`).
- **Resolution Status:** `RESOLVED`.

---

## 3. Residual Risk & Limitations

1. **Isolation Proof:** Isolation boundaries (cgroups, `--network none`, `--read-only`) are mathematically specified in code and CLI arguments, but cannot be claimed as empirically proven in this environment until the owner starts a real container daemon.
2. **Untrusted Code Integrity:** No untrusted repository code was executed with host privileges during this audit.
