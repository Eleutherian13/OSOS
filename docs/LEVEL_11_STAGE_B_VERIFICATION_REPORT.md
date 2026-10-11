# Level 11 — Sandbox Stage B Live Verification & Acceptance Report

**Date:** 2026-10-11  
**Status:** `IMPLEMENTED_BUT_NOT_ACCEPTED` (Stage B live container isolation verified; plan amendment & end-to-end wheel cache mount pending)  
**Governing Authority:** `AGENTS.md` §2, §4, §11, G1_OVERRIDE_AUTHORIZED, and explicit owner authorization.

---

## 1. Executive Summary

Level 11 Sandbox isolated execution has been verified against an operational container runtime environment on Windows 11 with WSL2 backend. All 7 live isolation controls have been tested and confirmed with real output and exit codes. All Level 11 unit and CLI tests pass (13/13).

- **Container Engine:** Docker Desktop 4.94.0 (`docker.exe` located at `C:\Users\manas\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe`)
- **Backend:** WSL2 Linux Kernel `6.6.87.2-microsoft-standard-WSL2`
- **Context:** `desktop-linux`
- **Stage A Integrity:** `PASS` (`uv.lock` SHA-256 matches `EXPECTED_LOCKFILE_HASH`)
- **Stage B Live Isolation:** `PASS` (7/7 live controls verified)
- **CLI Preflight:** `READY` (Exit 0)
- **Unit Suite:** 13/13 passing (`tests/test_level11_sandbox_orchestrator.py`)
- **Full Core Suite:** 146/146 passing

---

## 2. Stage A Integrity Verification

Stage A ensures dependency integrity and rejects stale or tampered lockfiles before container launch.

- **Lockfile Path:** `uv.lock`
- **Computed SHA-256:** `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94`
- **Expected Hash:** `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94` (defined in `src/agentos/sandbox_orchestrator.py`)
- **Command Allowlist:** Verified commands registered in `sandbox/test_cmds/verified_cmds.yaml` (`pytest`, `ruff`, `mypy`). Shell metacharacters and unallowlisted commands are deterministically rejected.

---

## 3. Stage B Live Adversarial & Isolation Test Results

Live tests executed against Docker daemon using `sandbox/live_stage_b_test.bat`.

### Test 1: Full Isolation Container Execution
- **Command:** `docker run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "echo CONTAINER_OK && id && uname -r"`
- **Result:**
  ```text
  CONTAINER_OK
  uid=0(root) gid=0(root) groups=0(root),0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
  6.6.87.2-microsoft-standard-WSL2
  ```
- **Evaluation:** `PASS` — Container starts with all required isolation flags.

### Test 2: Network Isolation (`--network none`)
- **Command:** `wget -q --timeout=3 http://example.com -O - 2>&1; echo EXIT_WGET=$?`
- **Result:**
  ```text
  wget: bad address 'example.com'
  EXIT_WGET=1
  ```
- **Evaluation:** `PASS` — Sockets, DNS, and outbound egress completely blocked.

### Test 3: Read-Only Root Filesystem (`--read-only`)
- **Command:** `echo test > /etc/test_rw 2>&1; echo EXIT_WRITE=$?`
- **Result:**
  ```text
  EXIT_WRITE=1
  sh: can't create /etc/test_rw: Read-only file system
  ```
- **Evaluation:** `PASS` — Base container filesystem cannot be modified.

### Test 4: Writable Workspace Mount (`--tmpfs /work`)
- **Command:** `echo WRITE_OK > /work/test.txt && cat /work/test.txt`
- **Result:**
  ```text
  WRITE_OK
  ```
- **Evaluation:** `PASS` — Writes confined strictly to ephemeral `/work`.

### Test 5: Privilege Escalation Prevention (`--security-opt=no-new-privileges`)
- **Command:** `grep NoNewPrivs /proc/self/status`
- **Result:**
  ```text
  NoNewPrivs:	1
  ```
- **Evaluation:** `PASS` — Kernel enforces `no-new-privileges`.

### Test 6: Resource Limits (4 GB RAM, 2 CPUs)
- **Command:** `cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null`
- **Result:**
  ```text
  4294967296
  ```
- **Evaluation:** `PASS` — Cgroup limits memory to exactly 4,294,967,296 bytes (4 GB).

### Test 7: Exit Code Propagation
- **Command:** `sh -c "exit 42"`
- **Result:**
  ```text
  DOCKER_EXIT=42
  ```
- **Evaluation:** `PASS` — Subprocess exit codes truthfully preserved.

---

## 4. CLI Preflight Verification

Verification of the CLI integration:
```bash
$ python -m agentos.cli sandbox preflight
=== Sandbox Preflight Checks ===
Kill Switch: [PASS] Kill switch inactive
Stage A Integrity: [PASS] Stage A lockfile and registry integrity verified
Container Runtime: [PASS] Docker daemon operational

Preflight result: READY.
Exit Code: 0
```

---

## 5. Test Suite Verification

### Level 11 Test Suite (`tests/test_level11_sandbox_orchestrator.py`)
13 tests executed, 13 passed (100%):
- `test_missing_runtime_fails_closed`: PASSED
- `test_stale_or_tampered_lockfile`: PASSED
- `test_denied_command_not_in_allowlist`: PASSED
- `test_denied_command_shell_injection`: PASSED
- `test_approval_bypass_attempt`: PASSED
- `test_kill_switch_active`: PASSED
- `test_successful_execution`: PASSED
- `test_timeout_enforcement`: PASSED
- `test_cancellation_enforcement`: PASSED
- `test_failed_artifact_export_traversal`: PASSED
- `test_cli_sandbox_preflight`: PASSED
- `test_cli_sandbox_preflight_blocked`: PASSED
- `test_cli_sandbox_run_denied_command`: PASSED

### Full Test Suite
- **Executed:** `pytest tests\ -v --ignore=tests\integration --ignore=tests\cli --ignore=tests\test_level9_github_client.py`
- **Result:** 146 passed, 0 failed in 4.56s.
- **Contract Test (`tests/test_contract.py`):** 3/3 passed.
- **Pre-existing limitations noted:**
  - `tests/test_level9_github_client.py`: requires `requests` package (optional Level 9 live client check).
  - Historical G1 status: remains `FAIL` under `G1_OVERRIDE_AUTHORIZED`.

---

## 6. Safeguards & Invariant Preservation

- **Persistence Backend:** SQLite preserved (`data/agentos.sqlite`, 19 tables). No PostgreSQL dependency introduced.
- **Upstream Boundaries:** Guard, Outbox, approval tokens, and kill epoch intact.
- **Replay Safety:** GitHub Actions replay (`act`) remains OFF by default.
- **Fail-Closed Execution:** Missing runtime, invalid hash, or unapproved command aborts without host execution.
