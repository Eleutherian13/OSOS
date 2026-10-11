"""Live Stage B execution: offline install + real pytest against L11 tests."""
import tarfile, io, subprocess, os, pathlib

repo = pathlib.Path.cwd()
src = repo / "tests" / "test_level11_sandbox_orchestrator.py"
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as tar:
    tar.add(src, arcname="tests/test_level11_sandbox_orchestrator.py")
tar_bytes = buf.getvalue()

sh_cmd = (
    "export PYTHONUSERBASE=/work/.local && "
    "export PYTHONPATH=/work/.local/lib/python3.12/site-packages && "
    "export PATH=/work/.local/bin:$PATH && "
    "pip install --user --no-index --find-links=/deps pytest 2>&1 | tail -1 && "
    "python -m pytest tests/test_level11_sandbox_orchestrator.py::test_missing_runtime_fails_closed tests/test_level11_sandbox_orchestrator.py::test_cli_sandbox_run_denied_command -v"
)
docker = str(pathlib.Path("C:\\Users\\manas\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"))
cmd = [
    docker, "run", "--rm", "-i", "--network", "none", "--read-only",
    "--tmpfs", "/tmp:rw,nosuid,size=1g", "--tmpfs", "/work:rw,exec,nosuid,size=4g",
    "--cpus", "2", "--memory", "4g", "--security-opt", "no-new-privileges",
    "-v", "agentos_sandbox_deps:/deps:ro", "-w", "/work",
    "python:3.12-slim", "sh", "-c", sh_cmd,
]
env = dict(os.environ, PATH=docker.rsplit(os.sep, 1)[0] + os.pathsep + os.environ["PATH"])
res = subprocess.run(cmd, input=tar_bytes, capture_output=True, timeout=300, env=env)
print(res.stdout.decode(errors="replace")[-2500:])
print("EXIT:", res.returncode)
