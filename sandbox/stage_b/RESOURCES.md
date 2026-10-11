# Stage B — Resource limits (design; BLOCKED)
# Spec: 2 CPU / 4 GB / 30 min max; apply at OS/container layer; child processes terminate with parent; capture termination reason / exit / resource use.
# Not enforceable via Python timeout alone (§D — insufficient for containment).
# Actual enforcement: NONE (no container / cgroups / ulimit available verified; not invented).

cpu_limit: 2 (container --cpus=2 intended; not active)
mem_limit: 4GB (container --memory=4g intended; not active)
wall_time_limit: 30min (container timeout / kill intended; not active)
enforcement_layer: container / OS (absent)
child_termination_guarantee: container kill + pid namespace; not present
capture_exit_status: planned (bounded stdout/stderr + exit code recording)
actual_status: BLOCKED (no runtime)
