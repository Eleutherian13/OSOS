# Stage B — Filesystem isolation (design; execution BLOCKED — no runtime)
# Requirements (§B): ro base FS; writable /work only; no host mounts; no home/SSH/cloud/cred access; symlink traversal prevented; disposable workspace.
# Enforced by: container runtime (absent) — not by application code alone.
# Current state: NOT ENFORCED (correctly reported — no false claim).

base_fs: read-only (intended; container layer)
work_dir: /work (or sandbox/work/ mapped inside container)
host_mounts: none (intended; container --mount empty / deny all)
path_traversal_prevention: int container chroot + read-only root; not claimed from app layer alone
workplace_disposable: yes (container per-run)
actual_enforcement: BLOCKED (no container)
