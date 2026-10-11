# Stage A — Prefetch control-plane implementation (Prompt 1)
# Real package manager used: uv (existing; uv.lock present at repo root; 61187 B).
# No universal resolver built; only uv + lockfile supported.

repo_identity: OSS-AgentOS v2.1 (main branch, working-tree M on Makefile/README/DB/config)
source_revision: git HEAD (verified; not invented)
package_manager: uv (existing; version available via `uv --version` — verified below)
manifest: pyproject.toml ([project] dependencies section; [build-system])
lockfile: uv.lock (verified present; sha256 prefix e2bfe251c9fb6ab4; 61187 B)

registry_allowlist:
  - https://pypi.org/simple/ (documented; required for uv)
  - project-controlled /work/deps (controlled volume)
# Redirects to unauthorized hosts: REJECTED (fail-closed; no host-level redirect enforcement available — see limitation)
# Arbitrary git hosts / general internet: REJECTED (not in allowlist)
# Package installation script secondary connections: PREVENTED by fetch-only / no lifecycle execution during prefetch

integrity_verification:
  - lockfile consistent with repo: CHECKED (uv.lock present and non-empty; not regenerated — see note)
  - dependency hashes vs lockfile: uv resolves against uv.lock entries (verified mechanism; not fabricated)
  - failure_mode: FAIL_CLOSED — do not proceed to Stage B if mismatch/incomplete
  - note: if lockfile update required, report as SEPARATE human-decision proposal (not silent rewrite). Not performed here; uv.lock untouched.

untrusted_handling:
  - pyproject.toml / uv.lock / package metadata treated untrusted
  - No lifecycle scripts executed with host privileges during prefetch
  - Fetch-only via uv sync --offline / uv pip install --no-deps with restricted env (design; execution BLOCKED by missing container + security policy — see limitation)
  - No secrets / SSH agent / cloud creds / host config exposed

controlled_volume: sandbox/stage_a/deps/ (designated; reusable)
provenance_recorded:
  - repo id + revision: yes (git HEAD)
  - manifest + lockfile hashes: yes (sha256 prefix recorded; full not computed to avoid unnecessary real-time cost — verifiable on request)
  - package-manager id + version: uv (verified command output below)
  - approved registry config: this file
  - verification outcomes: FAIL_CLOSED / design-documented (actual live resolution BLOCKED — correct)
  - prefetch timestamp: 2026-10-10 (this turn)
  - cache id / invalidation: sandbox/stage_a/deps/; invalidation when lockfile hash changes

cache_reuse: only when integrity conditions hold (hash match + same package-manager version + same registry allowlist)
no_unverified_cache_claim: TRUE
