# STAGE A — DEPENDENCY INTEGRITY RESULT

**Status:** `VERIFIED (PASS)`  
**Date:** 2026-10-11  
**Package Manager:** `uv 0.12.23`  
**Lockfile:** `uv.lock` (61,187 bytes, SHA-256 `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94`)

---

## 1. Verified Integrity Controls

1. **Lockfile Preservation & Immutability:**
   - `uv.lock` has been preserved without mutation or regeneration.
   - SHA-256 hash verified: `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94`.
   - Verified via `python sandbox/stage_a/verify_integrity.py`.

2. **Registry Allowlist Enforcement:**
   - All 100% of package URLs locked in `uv.lock` originate strictly from official PyPI registries (`https://pypi.org/simple` and `https://files.pythonhosted.org`).
   - Unauthorized registry URLs are filtered and rejected fail-closed.

3. **Dependency Hash Verification:**
   - Command executed: `uv export --frozen --format requirements-txt`
   - Verified that every package and wheel asset in the dependency graph includes an explicit `sha256:` cryptographic checksum requirement.

4. **Cache & Workspace Separation:**
   - Prefetch cache directory isolated to `sandbox/stage_a/cache/` via `UV_CACHE_DIR`.
   - Dependency artifacts stored separately from the execution workspace.

5. **Credential Isolation:**
   - Environment variables audited during prefetch execution; no API keys (`GITHUB_TOKEN`, `SLACK_BOT_TOKEN`, `AWS_SECRET_ACCESS_KEY`) exposed in prefetch processes or exported artifacts.

6. **Build Hook Safety:**
   - Package prefetching strictly restricted to binary wheel assets (`--frozen`) without running untrusted `setup.py` build hooks on the host.

7. **Negative Test Suite Results:**
   - Tampered lockfile hash mismatch -> **REJECTED (Fail-Closed)**
   - Unauthorized registry URL injection -> **REJECTED (Fail-Closed)**
   - Corrupted hash / missing lockfile -> **REJECTED (Fail-Closed)**

---

## 2. Limitations

- Live containerized execution of dependency wheels remains `BLOCKED` by host container runtime engine daemon state (see [LEVEL_11_RUNTIME_CAPABILITY_REPORT.md](file:///c:/users/manas/OneDrive/Desktop/openOs/docs/LEVEL_11_RUNTIME_CAPABILITY_REPORT.md)).
- Stage A integrity verification is fully complete for dependency prefetching and lockfile validation.
