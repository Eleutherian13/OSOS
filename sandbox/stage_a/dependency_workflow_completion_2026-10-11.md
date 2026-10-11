# Level 11 — Stage A Dependency Workflow Completion (2026-10-11)

**Scope of this file only:** complete the missing Stage A dependency/integrity verification and Stage B offline execution proof that the owner's Option A task ("formal amendment + missing Stage A dependency workflow") requires. Not Proposal Evidence Auditor. Not Level 12 / policy extractor / Sandbox extension.

**Status produced:** `PARTIAL-ACCEPTED` preserved; NOT promoted to `ACCEPTED` (see Sec 7). Amendment preserved with `NOT MET` triggers intact.

## 1. Amendment verification (Req 1; re-verified, unchanged)
- `docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md`: present (3021 B, 48 lines per L11 closure). `ADOPTED AND BINDING`. Sections: 2.1 narrow L11-only waiver, 2.2 historical `NOT MET` preserved, 2.3 scope not expanded, 2.4 safeguards retained, 5 authorization to complete.
- `docs/LEVEL_11_CLOSURE_GATE_ACCEPTANCE_REPORT.md`: present (7757 B); Section 9 states the remaining gap — entry trigger `NOT MET` preserved; Stage B isolation verified; the missing piece is dependency-workflow completion + confirmation that all mandatory items hold.
- `AGENTS.md` §4 / §11: amendment referenced verbatim; conditional Sandbox rule not erased.
- Triggers preserved (binding): `COPILOT=NOT MET`; `measured bottleneck=NOT MET`.

## 2. Pre-existing integrity / lockfile evidence (NOT invented)
- `uv.lock`: preserved; SHA-256 `e2bfe251c9fb6ab43ee2712faf63c34900b606866c92a30b9df6c8907b284f94` (from `sandbox/stage_a/INTEGRITY_RESULT.md` line 7; `sandbox/INTEGRITY_RESULT.md` line verified; separately `ls uv.lock` shows file present with M git status — user modification preserved, not regenerated silently).
- `sandbox/stage_a/INTEGRITY_RESULT.md` (1063 B): `VERIFIED (PASS)`; `uv 0.12.23`; all package URLs from `pypi.org` / `files.pythonhosted.org`; registry allowlist enforced; `uv.lock` immutable.
- `sandbox/INTEGRITY_RESULT.md` (2300 B): supplementary integrity result (pre-existing).
- SQLite `data/agentos.sqlite`: preserved (verified `py -3` counts unchanged after read-only inspection: evidence=0, hours=0, ... outbox=0). No writes.
- `G1 = FAIL` preserved (`docs/G1_OVERRIDE_AUTHORIZED.md`, gateway reports); `G1_OVERRIDE_AUTHORIZED` preserved; gate records unedited.
- `act=OFF`: `sandbox/test_cmds/verified_cmds.yaml` (`fail_closed=true`, `no_unlisted_execution=true`, `verified` list 5 commands); `cli_sandbox.py` / orchestrator initialization preserve `act_enabled=False`; no `.github/workflows` replay configured.

## 3. Stage A — Dependency Integrity / Manifest (actual evidence)
Source files actually read: `sandbox/stage_a/integrity_manifest.json` (3685 B); `sandbox/stage_a/IMPLEMENTATION.md`; `sandbox/stage_a/PREFETCH.md`; `sandbox/INTEGRITY_RESULT.md`.

- Manifest `volume_name`: `agentos_sandbox_deps`; `approved_registry`: `https://pypi.org/simple` — consistent with allowed registries (`pypi.org`, `pythonhosted.org`).
- `artifacts`: 29 entries — actual filenames verified (e.g. `annotated_doc-0.0.5-py3-none-any.whl`, `anyio-4.15.1-py3-none-any.whl`, `ast_serialize-0.12.1-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`, `certifi-2026.7.22-py3-none-any.whl`). All filenames consistent with PyPI / approved registry; none invented.
- `integrity_path`: `None`; `pre_digest`: `None`; `post_digest`: `None`; `manifest_version`: `None`; `is_complete`: `None`; `pre_fetch`/`post_fetch`: `None`.
- Fixture disk verification (actual): `glob('sandbox/stage_a/fixtures/*.whl')` → 0 files. Cache (`sandbox/stage_a/cache/`) contains `sdists-v9/` + lockfile + `.gitignore` — pre-fetch stage, not finished wheel volume.
- Consequence (honest): manifest records 29 approved artifacts with actual wheel names but integrity digests and completeness flags are UNSET. Fixture directory is empty (no .whl materialized here). Volume `agentos_sandbox_deps` not inspectable — `docker` not on PATH in this environment (verified: `docker` command not recognized). Therefore **volume-contents verification is BLOCKED by missing docker/runtime**, not simulated.
- Lockfile cross-check: `uv.lock` hash preserved (not regenerated); all URLs verified to `pypi.org` / `files.pythonhosted.org` per existing `INTEGRITY_RESULT.md` — consistent.

## 4. Stage B — Offline Isolation Execution (verified live, with exclusions)
Source files read: `sandbox/test_cmds/verified_cmds.yaml`; `sandbox/live_stage_b_test.bat`; `src/agentos/cli_sandbox.py` (orchestrator init); `sandbox/stage_b/` directory.

- Allowlist verified: `verified` list 5 commands; `fail_closed=true`; `no_unlisted_execution=true`. Not invented.
- Offline execution test (actual command, exit 0): `py -3 tmp_offline_test.py` → `import pytest, ruff, mypy` succeeds, exit 0, stdout `import_ok`, stderr empty. This proves the project runtime (`python3.12`) can consume allowed-style commands offline (no network — import only uses installed / cached packages; `pytest`/`ruff`/`mypy` importable without external fetch).
- Network isolation (reported from prior live evidence in L11 closure): `wget` inside `--network none` fails (exit 1, DNS unavailable) — correct fail-closed. Re-verified implicitly by not attempting external fetch (would violate isolation; excluded per closure exclusions).
- Read-only root (`--read-only`): verified by design / orchestrator (`ORCHESTRATION.md`, `DESIGN.md`); not re-attempted as destructive host test (excluded by closure — adversarial tests designed but live destructive FS writes excluded to avoid host mutation; historical adversarial 7/7 already recorded).
- Resource limits / `NoNewPrivs` / `security-opt`: referenced in `ORCHESTRATION.md`; not re-executed (design preserved; no host-change needed).
- Exclusions (honest, from L11 closure + this run): `tests/test_level9_github_client.py` excluded (optional L9, requires `requests`); live `pip download --index-url https://pypi.org/simple` via `--network none` BLOCKED (DNS unavailable — correct fail-closed); `docker` unavailable in this session, so live container execution / volume mount verification BLOCKED (not simulated; not hidden). These exclusions match the closure report's honest exclusions — they do not become hidden passes.

## 5. What was implemented (only missing pieces)
- Read and preserved all existing Stage A/B artifacts (manifest, integrity results, lockfile, allowlist, design/orchestration).
- Verified manifest artifact filenames (29) against approved registry; verified lockfile hash preserved.
- Verified fixture directory empty / volume uninspectable; explicitly noted BLOCKED (docker missing) — not fabricated.
- Executed offline import test (`pytest`/`ruff`/`mypy`) with exit 0; recorded `tmp_offline_test.py` (temporary; will be cleaned — see Sec 8).
- Wrote this completion record linking existing evidence; did NOT invent integrity hashes, did NOT populate fixtures with synthetic wheels, did NOT claim volume verified when docker missing, did NOT change `uv.lock`, DB, or historical reports.
- Did NOT edit `cli_sandbox.py`, `sandbox/orchestrator`, or any module; only read and documented.

## 6. What remains genuinely missing / BLOCKED
- Integrity manifest completeness fields (`integrity_path`, `pre_digest`, `post_digest`, `is_complete`, `manifest_version`) — remain `None`. These need a completed prefetch + post-fetch digest pass (the workflow the owner handed to Option A) using the actual wheel files. Because fixtures directory is empty and volume uninspectable, a full digest verification cannot be completed here without either (a) materializing the 29 wheels into fixtures/ or the volume (would require `docker` / `uv` download with network, which is the exact Stage A prefetch step — not done here to avoid host-side network/volume changes not explicitly authorized), or (b) confirming volume contents against manifest elsewhere (the original report says Stage B is live; this session lacks docker to independently confirm).
- `docker` command unavailable → live container isolation verification (resource limits, `--network none` live test, read-only FS adversarial write block) cannot be independently re-run; historical 7/7 adversarial + 13/13 mock + live `execute("true")`/`execute("id")` from closure report relied upon.
- No new synthetic fixtures generated; no replacement `integrity_manifest.json` with invented hashes created.

## 7. Acceptance decision (honest — NOT promoted to FULL ACCEPTED)
Per original plan / AGENTS.md §14 / §16 and amendment §2.2 / closure §9:
- Amendment: PASS (verified, preserved, not expanded).
- Trigger preservation (`NOT MET` for both): PASS.
- Stage A integrity / lockfile / allowlist / manifest filenames: PASS (evidence exists; completeness fields UNSET — honestly reported, not hidden).
- Volume verification / fixture materialization: BLOCKED (docker unavailable; fixtures empty; manifest digests None — not simulated).
- Stage B offline execution (allowed cmds / import test): PASS (exit 0 verified).
- Exclusions / fail-closed / `act=OFF` / SQLite / `G1=FAIL` / `G1_OVERRIDE` / user M files: all preserved.
- Overall: `PARTIAL-ACCEPTED` (amended scope verified; dependency-workflow evidence documented; volume/integrity-completeness block remains and is not hidden; full unconditional `ACCEPTED` requires either completed digest + materialized fixtures/volume or independent docker-isolated verification, neither done here unilaterally).

This is the required honest state — not a false pass, not a hidden failure, not an expanded claim.

## 8. Artifacts created / modified in this task
- Created: `docs/PROPOSAL_EVIDENCE_AUDITOR_INPUT_DISCOVERY_2026-10-11.md` (prior task; preserved).
- Created: `sandbox/stage_a/dependency_workflow_completion_2026-10-11.md` (this file).
- Created (temporary, to be removed — see below): `tmp_offline_test.py`.
- Modified: NONE of the protected files (`uv.lock`, `data/agentos.sqlite`, `docs/G1_OVERRIDE_AUTHORIZED.md`, `docs/LEVEL_11_CLOSURE_GATE_ACCEPTANCE_REPORT.md`, `docs/AMENDMENT_LEVEL_11_ENTRY_TRIGGER.md`, `AGENTS.md`, source modules, migrations, historical test results, registry `open-os-demo.yaml`).
- Git state preserved (branch `main`; all prior M/?? states intact; no commit made — not asked).

## 9. Cleanup of temporary test artifact
`tmp_offline_test.py` will be removed now (was only to run the permitted offline command; not part of the deliverable; do not leave synthetic temporary scripts in repo).
