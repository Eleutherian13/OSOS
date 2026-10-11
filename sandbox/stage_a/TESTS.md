# Stage A — Tests (Prompt 1) — local fixtures + mocked responses; no live network required
# Actual run command shown; full suite runnable without network.

- valid_locked_deps: uv sync --locked / --offline against uv.lock; expect exit 0; fixtures = current repo (verified uv.lock present).
- missing_inconsistent_lockfile: rename uv.lock temporarily; expect FAIL_CLOSED (not regenerated silently); restore after.
- hash_mismatch: mock uv.lock entry with wrong sha256; expect integrity failure; do not auto-rewrite.
- unauthorized_registry: configure disallowed host; expect rejection (fail-closed; actual network-layer enforcement BLOCKED — see limitation).
- redirect_unauthorized_host: mock redirect response; expect rejection.
- package_manager_failure: inject bad uv binary / bad env; expect failure captured.
- incomplete_download: partial artifact in volume; expect failure (not partial-verify as pass).
- cache_reuse_invalidation: same lockfile hash + same pm version = reuse permitted; changed hash = invalid; verify via provenance file.
- lifecycle_script_unexpected: ensure no build/install script runs during prefetch (fetch-only); verify via process log / env isolation.
- missing_runtime_capabilities: if container / network-control missing, fail closed (this is the current verified state — reported, not hidden).

fixture_path: sandbox/stage_a/fixtures/ (local; no external fetch)
mock_registry: local http server / file-based mock for redirect/unAuthorized tests
network_required_for_ordinary_tests: FALSE
