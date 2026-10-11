# STAGE A — DEPENDENCY INTEGRITY VERIFICATION RESULT

**Status:** `VERIFIED (PASS)`  
**Date:** 2026-10-11  
**Verification Script:** `sandbox/stage_a/verify_integrity.py`

## Verified Results

1. **Lockfile Hash:** `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94` (61,187 bytes). Lockfile preserved without rewrite or regeneration.
2. **Registry Allowlist:** Verified 100% of lockfile package source URLs originate from `https://pypi.org/simple` and `https://files.pythonhosted.org`.
3. **Cryptographic Checksums:** Verified via `uv export --frozen --format requirements-txt` that all dependencies require SHA-256 hash matching.
4. **Cache Directory:** `UV_CACHE_DIR` isolated to `sandbox/stage_a/cache/`.
5. **Credential Protection:** Zero tokens or secrets passed to prefetch processes.
6. **Untrusted Code Isolation:** Pre-built binary wheels prefetched without host execution of arbitrary package build scripts.
7. **Negative Tests:** Simulated hash tampered lockfile and unauthorized index injection both correctly rejected fail-closed.
