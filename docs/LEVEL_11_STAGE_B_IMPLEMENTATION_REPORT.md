# LEVEL 11 — STAGE B ISOLATED EXECUTION REPORT

**Status:** `BLOCKED (NOT ACCEPTED)` — Host Container Runtime Daemon Unavailable  
**Date:** 2026-10-11  
**Prerequisites:** [LEVEL_11_RUNTIME_INSTALL_REPORT.md](file:///c:/users/manas/OneDrive/Desktop/openOs/docs/LEVEL_11_RUNTIME_INSTALL_REPORT.md) | [LEVEL_11_RUNTIME_CAPABILITY_REPORT.md](file:///c:/users/manas/OneDrive/Desktop/openOs/docs/LEVEL_11_RUNTIME_CAPABILITY_REPORT.md)

---

## 1. Executive Summary & Fail-Closed Enforcement

Per `AGENTS.md` §11 (*"If the environment cannot enforce those controls, implement safe control-plane portions where useful and mark execution runtime BLOCKED. Never run untrusted repository code directly on the host to simulate a sandbox"*):

- **No Host Execution Fallback:** Untrusted repository code will **NOT** be executed on the Windows host to simulate a sandbox.
- **No Mocked Isolation Claims:** A mocked or stubbed container runtime is **NOT** accepted as real security isolation.
- **Current Runtime State:** Both Docker Desktop and Podman installation attempts require interactive Administrator UAC elevation on Windows 11. Until the daemon is started by the host owner, Stage B container execution is marked **`BLOCKED`**.

---

## 2. Stage B Security Controls Design Specification

When an operational container engine (`docker` or `podman`) is made available by the owner, Stage B enforces the following 11 mandatory boundary controls:

| Boundary Control | Enforcement Mechanism / Flag | Target Specification | Design Verification Status |
| :--- | :--- | :--- | :--- |
| **Network Isolation** | `--network none` | Zero inbound or outbound sockets | `DESIGNED (UNVERIFIED)` |
| **Read-Only Root FS** | `--read-only` | Root `/` strictly read-only | `DESIGNED (UNVERIFIED)` |
| **Writable Workspace** | `--tmpfs /work:rw,exec,nosuid,size=4g` | Ephemeral tmpfs at `/work` only | `DESIGNED (UNVERIFIED)` |
| **CPU Limit** | `--cpus 2` | Maximum 2.0 cores | `DESIGNED (UNVERIFIED)` |
| **Memory Limit** | `--memory 4g --memory-swap 4g` | 4 GB RAM, 0 swap overflow | `DESIGNED (UNVERIFIED)` |
| **Execution Timeout** | Subprocess wrapper (30 minutes) | SIGKILL after 1800 seconds | `DESIGNED (VERIFIED IN CODE)` |
| **Host Mount Isolation** | Zero `-v` volume mounts | No host paths, home, or SSH mounted | `DESIGNED (UNVERIFIED)` |
| **Unprivileged Mode** | `--security-opt=no-new-privileges` | No root escalation | `DESIGNED (UNVERIFIED)` |
| **Command Allowlist** | `sandbox/test_cmds/verified_cmds.yaml` | Only allowlisted commands run | `DESIGNED (VERIFIED IN CODE)` |
| **Artifact Export** | stdout/stderr stream extraction | No direct host filesystem write | `DESIGNED (VERIFIED IN CODE)` |
| **Container Cleanup** | `--rm` flag + container prune | Automatic cleanup on exit/timeout | `DESIGNED (UNVERIFIED)` |

---

## 3. Adversarial Test Suite Design

The following 10 adversarial test scenarios have been specified for execution once the runtime daemon is operational:

1. **Network Egress Attack:** Attempt `curl https://google.com` inside container -> Expected: `Network unreachable`.
2. **Root Filesystem Write Attack:** Attempt `touch /etc/malicious` -> Expected: `Read-only file system`.
3. **RAM Memory Exhaustion:** Allocate 6 GB RAM in container -> Expected: `OOM Killed`.
4. **CPU Bomb Attack:** Spin infinite loops across 8 threads -> Expected: Capped at 200% CPU (2 cores).
5. **Credential Exfiltration Attack:** Inspect container env for `GITHUB_TOKEN` / `.env` -> Expected: `Not found`.
6. **Host File Traversal Attack:** Attempt `ls /host` or access `C:\Users` -> Expected: `No such file or directory`.
7. **Command Injection Attack:** Pass `pytest; rm -rf /` -> Expected: Filtered by command allowlist parser.
8. **Symlink Traversal Attack:** Create symlink pointing outside `/work` -> Expected: Blocked by read-only root FS.
9. **Child Process Persistence Attack:** Fork background daemon inside container -> Expected: Destroyed on container exit.
10. **Timeout Kill Test:** Run `sleep 3600` inside container -> Expected: Force killed at 30 minutes.

---

## 4. Current Stage B Acceptance Status

- **Stage B Container Execution:** `BLOCKED`
- **Adversarial Runtime Verification:** `BLOCKED` (Awaiting container daemon)
- **Host Execution Fallback:** `REFUSED` (Preserving security integrity)
- **Unresolved Findings:** None (Fail-closed policy correctly enforced).
