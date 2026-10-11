# LEVEL 11 — CLI AND ORCHESTRATION INTEGRATION REPORT

**Status:** `IMPLEMENTED (TESTS PASSING, RUNTIME BLOCKED FAIL-CLOSED)`  
**Date:** 2026-10-11  
**Integration Module:** `src/agentos/sandbox_orchestrator.py`  
**CLI Module:** `src/agentos/cli_sandbox.py` (Registered on `agentos` CLI in `src/agentos/cli.py`)  
**Test Suite:** `tests/test_level11_sandbox_orchestrator.py` (12/12 passing)

---

## 1. Fail-Closed Workflow Implementation

The sandbox orchestrator implements a deterministic, multi-stage fail-closed pipeline:

```
[Start]
   │
   ▼
[Kill Switch & Epoch Check] ──(Active)──► [DENY: 126 KILL_SWITCH_ACTIVE]
   │ (Inactive)
   ▼
[Action Class Validation] ──(L3/L4 Upstream)──► [DENY: 126 APPROVAL_BYPASS_ATTEMPT_DENIED]
   │ (L1 Isolated)
   ▼
[Stage A Dependency Integrity] ──(Tampered/Stale)──► [FAIL: 1 INTEGRITY_CHECK_FAILED]
   │ (Hash & PyPI Allowlist OK)
   ▼
[Command Allowlist Check] ──(Unlisted/Injected)──► [DENY: 127 COMMAND_DENIED]
   │ (Allowlisted: pytest, ruff, mypy)
   ▼
[Container Runtime Preflight] ──(No Daemon)──► [FAIL-CLOSED: 125 RUNTIME_UNAVAILABLE]
   │                                             *(Strictly NO host fallback)*
   │ (Daemon Operational)
   ▼
[Create Unique Workspace] -> sandbox/work/<run_id>
   │
   ▼
[Stage B Container Execution]
   │ - --network none
   │ - --read-only
   │ - --tmpfs /work:rw,exec,nosuid,size=4g
   │ - --cpus 2 --memory 4g
   │ - --security-opt=no-new-privileges
   │ - 30-min timeout / process isolation
   ▼
[Validate & Export Artifacts] ──(Traversal detected)──► [FAIL: 1 EXPORT_FAILED]
   │ (Relative paths OK)
   ▼
[Reliable Workspace Cleanup] ──(finally block: rmtree sandbox/work/<run_id>)
   │
   ▼
[Truthful Result Capture] (status, exit_code, stdout, stderr, duration)
```

---

## 2. CLI Registration & Commands

The CLI commands are registered under `agentos sandbox`:

1. `agentos sandbox preflight`:
   Runs the full preflight chain (Kill Switch, Stage A Integrity, Container Runtime).
   - If any prerequisite fails, exits with code 1.
   - Example run output on current Windows 11 host:
     ```text
     === Sandbox Preflight Checks ===
     Kill Switch: [PASS] Kill switch inactive
     Stage A Integrity: [PASS] Stage A lockfile and registry integrity verified
     Container Runtime: [BLOCKED] No container runtime (Docker/Podman) is operational
     Preflight result: BLOCKED (Fail-Closed). Execution disabled.
     ```

2. `agentos sandbox run <CMD>`:
   Executes an allowlisted command inside the isolated Stage B container.
   - Rejects unallowlisted commands (`COMMAND_DENIED`, exit 127).
   - Fails closed when runtime is unavailable (`RUNTIME_UNAVAILABLE`, exit 125).

---

## 3. Test Verification Results

All 12 targeted unit and integration tests passed in `tests/test_level11_sandbox_orchestrator.py`:

| Test Case | Description | Result | Exit Code / Status |
| :--- | :--- | :--- | :--- |
| `test_missing_runtime_fails_closed` | Missing daemon fails closed, no host execution | `PASS` | 125 `RUNTIME_UNAVAILABLE` |
| `test_stale_or_tampered_lockfile` | Modified lockfile hash fails Stage A | `PASS` | 1 `INTEGRITY_CHECK_FAILED` |
| `test_denied_command_not_in_allowlist` | Unlisted command rejected | `PASS` | 127 `COMMAND_DENIED` |
| `test_denied_command_shell_injection` | Shell metacharacters (`;`, `\|`) rejected | `PASS` | 127 `COMMAND_DENIED` |
| `test_approval_bypass_attempt` | L3/L4 upstream bypass blocked | `PASS` | 126 `APPROVAL_BYPASS_ATTEMPT_DENIED` |
| `test_kill_switch_active` | STOP state halts execution immediately | `PASS` | 126 `KILL_SWITCH_ACTIVE` |
| `test_successful_execution` | Operational runtime runs with 9 isolation flags | `PASS` | 0 `SUCCESS` |
| `test_timeout_enforcement` | Subprocess timeout produces code 124 | `PASS` | 124 `TIMEOUT` |
| `test_cancellation_enforcement` | SIGINT / KeyboardInterrupt produces code 130 | `PASS` | 130 `CANCELLED` |
| `test_failed_artifact_export_traversal` | Path traversal (`../../`) blocked | `PASS` | 1 `EXPORT_FAILED` |
| `test_cli_sandbox_preflight` | CLI preflight command exits non-zero on block | `PASS` | Exit 1 |
| `test_cli_sandbox_run_denied_command` | CLI run command rejects unlisted commands | `PASS` | Exit 127 |

Combined CLI suite run: `18 passed in 0.65s` (`test_cli.py` + `test_level11_sandbox_orchestrator.py`).
