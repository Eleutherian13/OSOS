# RUN_AND_USE_GUIDE.md — Verification Report

Created: 2026-10-14. Scope: beginner's run/operation/usage guide only; no application code, DB, test, migration, or security change.

## A. Inspection result (before edit)

- Existing user guide: none (`docs/RUN_AND_USE_GUIDE.md` did not exist; README served as entry point but was minimal).
- Existing README: `README.md` rewritten in prior turn to 393 lines / 32786 bytes; this task does not alter README further (only references it).
- Source verified: `AGENTS.md`; v2.1 plan references; `pyproject.toml`; `uv.lock`; `.env.example`; CLI modules (`cli_path`, `cli_readiness`, etc.); DB config/migrations; tests; `docs/PHASE_9_*.md`; current `README.md`.
- No external browse performed (offline design per task; no fabricated URLs).

## B. Documented workflows

| Workflow | Implementation | Tests | Evidence | Status in guide |
|---|---|---|---|---|
| Check environment (python/uv/files) | Confirmed | — | Actual commands | Documented, verified |
| Open project directory | Confirmed | — | Actual paths | Documented |
| Configure DB path (AGENTOS_DB_PATH) | Confirmed (`db/config.py`) | — | Source + .env.example | Documented |
| Initialize DB (migrations V001..V012) | Confirmed (`migrations/` + runner) | `test_level2_3_integration.py` | P9-1 output (`tmp_p9_migration_output.txt`) | Documented; V011/V012 gap noted |
| Start session / CLI help | Confirmed (entry points exist) | — | `cli_path --help`; `pyproject.toml` scripts | Documented |
| Synthetic path + interaction + evidence | Confirmed (schema; source) | Synthetic fixtures (labelled) | Source contracts | Documented; synthetic clearly labelled |
| Read state / inspect DB | Confirmed (`sqlite3`) | — | Actual commands shown | Documented |
| Run focused tests | Confirmed (pytest collections) | 15 auditor; guard; budget; integration | `tmp_p9_regression_summary.txt` | Documented; historical failures preserved |
| Security / act=OFF / Guard / Outbox | Confirmed (source + tests + docs) | `test_guard.py`; P7 reports | `docs/P7_FINAL_ACCEPTANCE.md` | Documented; not weakened |
| Stop / restart / reset (disposable) | Confirmed (file-based SQLite) | — | Actual commands safe | Documented; production preserved |

Not documented as verified (correctly blocked/unverified): full-suite PASS (would need disposable DB + pipeline fixtures; 5 historical failures preserved); live GitHub endpoint (act=OFF); benchmark evaluation (BLOCKED); evaluator (BLOCKED); real proposal E2E (BLOCKED).

## C. Command verification (actual runs)

- `python --version` → 3.14.0 (PASS)
- `uv --version` → 0.12.23 (PASS)
- `Test-Path` / `ls` checks for DB/file presence (PASS — file exists; DB preserved)
- `sqlite3` integrity / schema / FK checks (PASS — executed in P9-1; documented; not re-run; safe)
- `py_compile` on key files (PASS — P9-2)
- `pytest --co -q tests/test_auditor_domain.py` (PASS — 15 collected; exit 0; not full execution of every item)
- `ruff` / `mypy` (documented results — E702 reproduced; mypy blocked by missing file; no false PASS)
- Quick-start command sequences (syntax/arguments verified against source; no fabricated output claimed; output format described generically with "expected result" descriptions rather than fabricated exact lines)

Commands NOT executed (correctly): destructive DB reset; upstream post; benchmark computation; external endpoint call; full `pytest` suite reconciliation (would require disposable DB setup + time; documented as not claimed PASS).

## D. Claim verification (guide claims → source)

- "Evidence-driven contribution path management" → `AGENTS.md` §1/§6; source (evidence schema V003; provenance; append-only events) — PASS
- "Not generic automation" / "no fabricated benchmark" / "no synthetic as real" → `AGENTS.md` §6/§7; P9 reports (benchmark BLOCKED; evaluator BLOCKED; E2E BLOCKED); design A critic-only — PASS
- "G1 FAIL preserved; override ≠ pass" → `docs/G1_OVERRIDE_AUTHORIZED.md`; `docs/G0_G1_FINAL_STATUS.md`; README text — PASS
- "SQLite backend (binding); PG superseded" → `AGENTS.md` §5; `pyproject.toml`; `db/config.py`; actual DB at `data/agentos.sqlite` — PASS
- "P7 accepted; live endpoint preserved separately" → `docs/P7_FINAL_ACCEPTANCE.md`; `red_*.py`; `verify_adapter.py`; README "NOT reopened" — PASS
- "L9 benchmark BLOCKED (50 labeled)" → `docs/LEVEL_11_*.md`; `AMENDMENT` doc; matrix — PASS
- "L10/L12 evaluator BLOCKED (owner session + 7d)" → `LEVEL_10_GOLDEN_ANSWERS.md`; `owner_labelling_session*.md`; matrix — PASS
- "L16 Design A PASS / E2E BLOCKED; Design B deferred" → `PHASE_8_FINAL_ACCEPTANCE.md` §3/§5; `auditor_service` edit; DB `evidence=0` — PASS
- "L14 preserved-not-expanded; L13/L15 deferred" → `AGENTS.md` §4; matrix; documentation — PASS
- "Six corrections embedded" → `PHASE_9_EXECUTION_PLAN_CORRECTION.md`; matrix — PASS
- "Quick-start uses `uv` / `python` / `sqlite3`" → actual commands shown; PASS
- "Status table matches matrix" → cross-referenced to `PHASE_9_CANONICAL_STATUS_MATRIX.md` — PASS
- "Mermaid diagram reflects actual architecture" → nodes match source modules (CLI, SQLite, core services, guard, outbox, ranking, auditor, event_store, watch, human auth, benchmark block) — PASS (not used in guide; kept in README)
- "No unauthorized upstream / act=OFF preserved" → `AGENTS.md` §7; `docs/LEVEL_11_SANDBOX_*.md`; README — PASS
- "No fake badges / outputs / user counts" → intentionally omitted; status table used — PASS
- "No fabricated command outputs" → output descriptions generic; no invented exact terminal lines — PASS

## E. Links and assets

- All internal links reference existing files: `AGENTS.md`, `README.md`, `pyproject.toml`, `docs/PHASE_9_*.md`, `tests/`, `src/agentos/db/sqlite_migrations/`, `migrations/`, `data/agentos.sqlite`, `config/`, `.env.example`.
- No new image/SVG needed (mermaid in README; text + table sufficient for guide).
- No external image URLs invented.

## F. Safety review

- `act=OFF` preserved: guide explicitly states no upstream; no command enables it; reset section does not suggest changing it.
- No secret shown: `.env.example` shown conceptually (`AGENTOS_DB_PATH`); `.env` excluded; no credential in examples.
- Database safety: disposable-file procedure emphasized; production file (`data/agentos.sqlite`) explicitly protected; never asked to delete production.
- No destructive command recommended as routine: reset requires disposable file + new name; never "delete DB."
- Guard/authorization preserved: guide explains denial means effect did not occur; not weakened.
- G1 / P7 / P8 / Design B / L13/L14/L15 status preserved correctly in guide references.

## G. Limitations (explicit, not hidden)

- Full first-run demonstration of complete CLI→repository→evidence→readiness→watcher→guard→outbox chain as a single automated execution: NOT EXECUTED (would need synthetic fixtures + service init + controlled sequence). Individual steps verified; combined replay documented as required but not fabricated.
- Real proposal E2E (L16): BLOCKED — prerequisites listed; guide directs to `docs/PHASE_9_FINAL_ACCEPTANCE.md` §5 rather than inventing inputs.
- Benchmark / evaluator: BLOCKED — prerequisites named; guide does not invent labels or session evidence.
- No external renderer preview (Markdown renders via GitHub; syntax correct; mermaid not needed here).
- No full `pytest` suite PASS claimed (historical failures preserved per P9-2).
- No web fetch / external benchmark data used (offline design correct; no dependency on live services for guide function).

## H. Change inventory

- `docs/RUN_AND_USE_GUIDE.md` — new (701 lines); beginner's usage guide.
- `README.md` — unchanged by this task (rewritten in prior turn; verified; referenced by guide).
- `docs/README_VERIFICATION_REPORT.md` — new (verification of README; separate from guide verification).
- No other file changed; no DB modified; no git mutation; no upstream.

## I. Final quality-gate result

- Zero unsupported factual claims (each mapped to source/test/status doc).
- Zero false "PASS" or "complete" claims where evidence missing.
- Zero fabricated screenshots, badges, outputs, counts, or user narratives.
- All referenced local links resolve to existing files.
- All documented commands verified safe; none require secrets/network/authorization to run.
- Controlled-language format applied (short sentences, active voice, one action/step, terms defined at first use).
- Safety controls (act=OFF, Guard, DB, G1, P7) preserved; not weakened for guide convenience.
- Status transparency: BLOCKED, DEFERRED, FAIL, NOT_VERIFIED all preserved and explained.
- Directory structure preserved (no new subsystems; L13/L14/L15/Design B not started).

Status: GUIDE ACCEPTED — documentation task complete; no new implementation; no claim of full application readiness; limitations named; evidence preserved.
