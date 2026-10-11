import subprocess
import os
import pathlib
from agentos.sandbox_orchestrator import SandboxOrchestrator

orch = SandboxOrchestrator()
engine = orch._resolve_docker_binary()
env = orch._get_runtime_env(engine)

# 1. create volume
v_res = subprocess.run([engine, 'volume', 'create', 'agentos_sandbox_deps'], capture_output=True, text=True, env=env)
print('Volume create:', v_res.returncode, v_res.stdout.strip())

# 2. pip download into /deps
sh_cmd = 'pip download --only-binary=:all: --no-build-isolation --index-url https://pypi.org/simple -d /deps typer pydantic pyyaml httpx pytest ruff mypy && ls -la /deps'
cmd = [
    engine, 'run', '--rm',
    '-v', 'agentos_sandbox_deps:/deps',
    'python:3.12-slim',
    'sh', '-c', sh_cmd
]
res = subprocess.run(cmd, capture_output=True, text=True, env=env)
print('Download exit code:', res.returncode)
print('Stdout:\n', res.stdout[:500])
if res.stderr:
    print('Stderr:\n', res.stderr[:500])
