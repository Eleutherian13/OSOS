@echo off
set DOCKER=C:\Users\manas\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe

echo === LIVE STAGE B ISOLATION TESTS ===
echo.

echo --- Test 1: Basic container execution with all isolation flags ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "echo CONTAINER_OK && id && uname -r"

echo.
echo --- Test 2: Network isolation verification (should FAIL - no network) ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "wget -q --timeout=3 http://example.com -O - 2>&1; echo EXIT_WGET=$?"

echo.
echo --- Test 3: Read-only root filesystem (should fail to write to /etc) ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "echo test > /etc/test_rw 2>&1; echo EXIT_WRITE=$?"

echo.
echo --- Test 4: Writable /work only ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "echo WRITE_OK > /work/test.txt && cat /work/test.txt"

echo.
echo --- Test 5: No new privileges (no-new-privileges flag) ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "id && grep NoNewPrivs /proc/self/status"

echo.
echo --- Test 6: CPU/Memory limits visible ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null"

echo.
echo --- Test 7: Exit code preserved ---
%DOCKER% run --rm --network none --read-only --tmpfs /work:rw,exec,nosuid,size=4g --cpus 2 --memory 4g --security-opt=no-new-privileges -w /work alpine:latest sh -c "exit 42"
echo DOCKER_EXIT=%ERRORLEVEL%
