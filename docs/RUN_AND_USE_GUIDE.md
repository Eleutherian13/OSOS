# OSS-AgentOS v2.1 — Beginner's Run, Operation & Usage Guide

> A practical guide for a new user. It teaches what OSS-AgentOS does, how to prepare, how to run verified steps, and where the limits are. It does not claim capabilities that have not been verified.

This guide is written in controlled language (short sentences, direct verbs, one action per step, terms defined at first use) so a beginner can follow it without guessing. It protects the project's safety rules and does not invent features.

- [What OSS-AgentOS is](#what-oss-agentos-is)
- [What the system does not do](#what-the-system-does-not-do)
- [Before you start](#before-you-start)
- [How to open the project](#how-to-open-the-project)
- [How to check your computer](#how-to-check-your-computer)
- [How to install](#how-to-install)
- [How to configure safely](#how-to-configure-safely)
- [How to initialize the database](#how-to-initialize-the-database)
- [How to start a first session](#how-to-start-a-first-session)
- [How to run a verified workflow](#how-to-run-a-verified-workflow)
- [How to understand the results](#how-to-understand-the-results)
- [How to inspect state](#how-to-inspect-state)
- [How to run tests](#how-to-run-tests)
- [How to stop safely](#how-to-stop-safely)
- [How to restart](#how-to-restart)
- [How to reset cleanly only when safe](#how-to-reset-cleanly-only-when-safe)
- [Security boundaries](#security-boundaries)
- [Common errors and fixes](#common-errors-and-fixes)
- [Glossary](#glossary)
- [Where to go next](#where-to-go-next)

**Important — read first:** This guide describes what the current repository does. It does not describe future work that is not yet implemented. For full status (implemented / verified / blocked / deferred), see [`docs/PHASE_9_CANONICAL_STATUS_MATRIX.md`](docs/PHASE_9_CANONICAL_STATUS_MATRIX.md) and [`README.md`](README.md). For the security rules, see `AGENTS.md`. The project uses SQLite (not PostgreSQL) and has `act=OFF` (no automatic upstream actions).

---

## What OSS-AgentOS is

OSS-AgentOS is a system that helps manage open-source contribution paths. A **path** is a planned contribution from a mentor to a project. The system records:

- The path definition (mentor, project, type, state).
- Mentorship interactions (email, issue, pull request, meeting, other).
- Evidence links (file and line references, quotes, timestamps, provenance).
- Readiness assessments (a checklist of required items, with the lowest-unmet item reported first).
- Watcher events (changes to tracked pages, with diffs when changed; zero writes when unchanged).
- Guard decisions (authorization checks that deny unauthorized actions).
- Outbox drafts (proposed upstream actions that are not sent until authorized).

The system is built in **levels** (v2.1). Each level is a small, complete part. Later levels extend earlier ones. The system is evidence-driven: it records where information came from, and it requires real evidence for evaluation claims.

A beginner can use it to create a path, log interactions, record evidence, check readiness, and inspect results — all with local SQLite storage and no required external service.

---

## What the system does not do

Do not assume any of the following. The code does not support them in the current checkout, and they are not promised for a beginner's first session:

- It does not generate mentor replies for you.
- It does not post to GitHub (issues, comments, PR reviews) automatically. The `act=OFF` setting prevents this.
- It does not create pull requests automatically.
- It does not fabricate benchmark labels, quiz answers, or review findings.
- It does not evaluate a proposal automatically against a fake dataset. The Proposal Auditor (Level 16, Design A) is critic-only and reads real input files; it does not invent proposal content.
- It does not replace a database server with a new one — SQLite is the verified backend.
- It does not complete every evaluation gate automatically. Some gates require genuine human labels or real source evidence that has not yet been provided.

If you need those capabilities, you must provide the required inputs and authorization — not just change a setting.

---

## Before you start

**You need:**

- A computer with Windows PowerShell, Linux terminal, or macOS terminal (this guide uses Windows PowerShell syntax because the environment is Windows; adapt paths for your system).
- Python 3.12 or newer. The repository specifies `>=3.12,<3.13`; the verification environment has 3.14.0 which works.
- `uv` (the package manager). The repository uses `uv` and `uv.lock`.
- A terminal open in the project directory.
- No PostgreSQL service is required. The project uses SQLite.

**You must understand:**

- A **virtual environment** is a separate folder that holds this project's Python packages so they do not mix with other projects. The repository uses `.venv/` (already present).
- A **database file** (`data/agentos.sqlite`) is where the system stores information locally. You can copy it safely for testing, but do not delete it without a backup.
- A **migration** is a controlled change to the database structure that is recorded and can be applied in order. The project has migrations V001 through V012.
- **Evidence** is a record that links a claim to a source file, line, quote, timestamp, and provenance. It is not a summary; it is a reference.
- **Provenance** tells you where the information came from and how the system got it.
- **`act=OFF`** means the system will not perform any upstream action (post, comment, merge) without your authorization.

---

## How to open the project

**Purpose:** Confirm you are in the right folder.

**Where to work:** The folder shown by your terminal when you started. The repository root is `C:\Users\manas\OneDrive\Desktop\openOs` in the verification environment.

**Steps:**

1. Open a terminal.
2. Confirm the current directory.

**Command:**

```powershell
Get-Location
```

**What to expect:** The path should end with `openOs` (or your project folder name). If it does not, use `Set-Location` to navigate.

**Why this matters:** All commands in this guide assume you are in the project root. The commands use relative paths (`data/agentos.sqlite`, `docs/PHASE_9_*.md`, `tests/`, `src/agentos/`). If you run them from a different folder, they will not find the files.

---

## How to check your computer

**Purpose:** Confirm that the required software exists before you try to install.

**Steps:**

1. Check Python.

```powershell
python --version
```

**Expected result:** A line like `Python 3.14.0`. If it says the command is not found, install Python 3.12 or newer from python.org.

2. Check the package manager.

```powershell
uv --version
```

**Expected result:** A version like `uv 0.12.23`. If it is missing, install `uv` (see `https://docs.astral.sh/uv/` — this is an external dependency; the guide does not include installation steps for `uv` itself because it is a package manager, not part of this project).

3. Check the project files.

```powershell
Test-Path README.md; Test-Path pyproject.toml; Test-Path uv.lock; Test-Path data/agentos.sqlite
```

**Expected result:** All four return `True`. The `data/agentos.sqlite` file is the production SQLite database (verified present at 286720 bytes; preserved in this session). If it is missing, see [How to initialize the database](#how-to-initialize-the-database) — do not invent a file.

**Safety note:** Do not modify `data/agentos.sqlite` as a routine step. It is the production database. For testing, create a separate file with a different name.

---

## How to install

**Purpose:** Install the project's Python dependencies using the verified package manager.

**Before you start:** Confirm steps from [How to check your computer](#how-to-check-your-computer) completed successfully.

**Where to work:** The project root (
`C:\Users\manas\OneDrive\Desktop\openOs` in this environment; use your folder).

**Steps:**

1. Install dependencies from the lockfile.

```powershell
uv sync
```

**What this does:** It reads `pyproject.toml` and `uv.lock` and installs the exact versions of `typer`, `pydantic`, `pyyaml`, `httpx`, and development tools (`pytest`, `ruff`, `mypy`). It uses the `.venv/` folder.

**Why this step matters:** The lockfile ensures that every user gets the same versions. Do not edit `uv.lock` to fix an installation error unless you understand dependency resolution. If `uv sync` fails, check whether Python is in your system PATH first.

**Expected result:** The command completes with no errors. It does not create or change the database.

**If the result is different:**
- If you see a version conflict, do not change dependencies. Check `pyproject.toml` for required versions.
- If `.venv/` is missing, the command creates it. That is expected.
- If a dependency download fails, check your network. The project does not require external services to install, only the package registry.

---

## How to configure safely

**Purpose:** Set the database path and any optional settings without exposing secrets.

**Before you start:** Installation completed. You have not started the application yet.

**What exists:**

- `.env.example` — a template with no secrets. It notes that `AGENTOS_DB_PATH` selects the SQLite file.
- `config/` — `budgets.yaml`, `prices.yaml`, `programs.yaml`. Do not edit these without understanding the budget/hour rules (`AGENTS.md` §5; `docs/PHASE_9_STATIC_CONFIG_SECURITY_REPORT.md`).

**What you must do:**

1. Decide whether to use the production database or a disposable test database.

   - For real use with your own data: use `data/agentos.sqlite` (default; do not delete it).
   - For safe testing: create a new file, for example `tmp/mytest.sqlite`, and use that path.

2. If using a disposable database, set the environment variable.

```powershell
$env:AGENTOS_DB_PATH = "tmp/mytest.sqlite"
```

**Why:** The application reads `AGENTOS_DB_PATH` through `agentos/db/config.py`. If it is not set, it uses the default from `cli_path.py` (`data/agentos.sqlite`). Setting it explicitly makes it clear which database you are using.

3. If using the production database, do not change `AGENTOS_DB_PATH`. Just be aware of which file you are working with.

4. Check that you have not accidentally put a secret into `.env`. The `.gitignore` excludes `.env` — do not commit it.

**Safety note:** The project has `act=OFF`. No command will post to GitHub or send a message automatically. You must explicitly approve any outward action through the Outbox and approval-token path. This is a feature, not a missing step.

---

## How to initialize the database

**Purpose:** Create or update the database structure using the actual migration system.

**Before you start:** The project is installed. You know which database file you want to use (production `data/agentos.sqlite`, or a disposable file). If using the production file, it is already initialized (verified by `sqlite3` schema inspection and P9-1 migration verification).

**Where to work:** Project root.

**What to understand:**

- A **migration** changes the database structure in a recorded order.
- The project has migrations `V001` through `V011` in `migrations/`, with SQLite-compatible versions in `src/agentos/db/sqlite_migrations/`. `V012` is in `sql_migrations/` (SQL-only; must be ported or applied manually for full sequence — documented in P9-1, not hidden).
- The runner applies them sequentially and verifies with `PRAGMA integrity_check`.

**Steps for a fresh disposable database:**

1. Create the directory and empty file.

```powershell
New-Item -ItemType Directory -Force -Path tmp
New-Item -ItemType File -Path tmp/mytest.sqlite
```

2. Set the environment variable.

```powershell
$env:AGENTOS_DB_PATH = "C:\Users\manas\OneDrive\Desktop\openOs\tmp\mytest.sqlite"
```

3. Apply migrations.

```powershell
uv run python -c "from agentos.db.config import DatabaseConfig; from agentos.db.migrations import run; import os; os.environ['AGENTOS_DB_PATH']='tmp/mytest.sqlite'; run(DatabaseConfig.from_env())"
```

**What this does:** It connects to the file you named, runs the SQLite migrations (V001–V010 verified in P9-1; V011 and V012 may require manual application — see Note below), and creates the schema.

**Expected result:** The command completes with no errors. The database file now contains tables (`paths`, `mentors`, `interactions`, `evidence`, `event_store`, etc.).

**How to check:**

```powershell
python -c "import sqlite3; c=sqlite3.connect('tmp/mytest.sqlite'); print('tables=', [r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")]); print('integrity=', c.execute('PRAGMA integrity_check').fetchone()[0]); print('FK=', len(c.execute('PRAGMA foreign_key_check').fetchall()))"
```

**Expected result:** A table count near 23 (for V001–V010 applied), `integrity=ok`, `FK=0`.

**Note — V011 and V012:** The SQLite migration directory (`sqlite_migrations/`) contains V001–V010. V011 (`quiz_items`) and V012 (`path_mentors` removal) are present in `migrations/` and `sql_migrations/` but not in the SQLite directory. The runner uses the SQLite directory when the DSN is `sqlite:///`. If you need V011/V012 for your use, apply them manually (for example, `sqlite3 tmp/mytest.sqlite < sql_migrations/V012__path_mentor_remove.sql`) after the runner completes. This is documented in `docs/PHASE_9_MIGRATION_RECOVERY_LOG.md`; it is not a hidden failure.

**Safety note:** This command creates/updates the file named by `AGENTOS_DB_PATH`. It does not touch `data/agentos.sqlite` unless you set the variable to that path. Before running on production data, create a backup copy of the production file.

---

## How to start a first session

**Purpose:** Reach a verified checkpoint where you can interact with the system.

**Before you start:** The project is installed. You have decided which database to use. The database is initialized (or was already present, as for `data/agentos.sqlite`).

**Where to work:** Project root.

**Steps:**

1. Confirm configuration.

```powershell
python -c "from agentos.db.config import DatabaseConfig; print(DatabaseConfig.from_env())"
```

**Expected result:** A line showing the SQLite path (e.g., `db_path='data/agentos.sqlite'`). If it raises `DatabaseConnectionError`, check that `AGENTOS_DB_PATH` is set (or use the default file).

2. Confirm the database is readable.

```powershell
python -c "import sqlite3; c=sqlite3.connect('data/agentos.sqlite'); print('readable:', c.execute('SELECT 1').fetchone()[0])"
```

**Expected result:** `readable: 1`. This confirms the SQLite adapter and file access work. It does not confirm that all migrations have been applied to this file (the production file should already be consistent; if you see missing tables, apply migrations before using it for writes).

3. Use a CLI command that reads safely.

```powershell
uv run python -m agentos.cli_path --help
```

**Expected result:** A help message describing commands (path creation, state inspection, evidence). If it fails with `ERROR: Set AGENTOS_DB_PATH or DATABASE_URL`, set the environment variable (see [How to configure safely](#how-to-configure-safely)).

**Checkpoint reached:** You have verified installation, configuration, database access, and CLI presence. The system is not yet performing unauthorized actions (act=OFF). You can proceed to learn the interfaces.

---

## How to run a verified workflow

The project supports several workflows. The most valuable beginner workflow is a **read-only inspection workflow**: create a test database, create a synthetic path, log a synthetic interaction, record synthetic evidence, check readiness, then inspect outputs. This uses only disposable state and requires no external service.

**What you need:** The project installed. A disposable database (see [How to initialize the database](#how-to-initialize-the-database)). `AGENTOS_DB_PATH` set to the disposable file.

**Purpose:** Learn the full pipeline without affecting production data or performing upstream actions.

**Steps:**

1. Confirm disposable database.

```powershell
$env:AGENTOS_DB_PATH = "tmp/guide_disposable.sqlite"
```

2. Apply migrations to the disposable file (if not already applied; if this is a fresh file created just now, apply them).

```powershell
uv run python -c "from agentos.db.config import DatabaseConfig; from agentos.db.migrations import run; import os; os.environ['AGENTOS_DB_PATH']='tmp/guide_disposable.sqlite'; run(DatabaseConfig.from_env())"
```

3. Create a synthetic path (read-only / write to disposable only). The CLI validates input; it requires valid state strings.

```powershell
# This command creates a record. It writes to the disposable file.
# The example uses synthetic identifiers (test_path_1, synthetic_mentor_1) — clearly labelled.
uv run python -c "
import sqlite3, os
os.environ['AGENTOS_DB_PATH']='tmp/guide_disposable.sqlite'
# Direct SQLite insert for demonstration (use CLI when available for full validation):
c=sqlite3.connect('tmp/guide_disposable.sqlite')
c.execute(\"INSERT INTO paths (id,org_id,project_id,mentor_id,path_type,path_slug,state) VALUES ('path_test_1','org_1','proj_1','mentor_1','gsoc','test-path','WATCH')\")
c.commit()
print('Synthetic path inserted:', c.execute('SELECT id, state FROM paths WHERE id=?', ('path_test_1',)).fetchone())
"
```

**Safety note:** This insert is a direct SQL demonstration for learning only. The production CLI (`cli_path`) performs validation (state enum check, unique constraint, foreign keys) which this direct insert skips. Use the CLI for real work.

4. Inspect the result.

```powershell
python -c "import sqlite3; c=sqlite3.connect('tmp/guide_disposable.sqlite'); print('paths=', c.execute('SELECT id,state FROM paths').fetchall())"
```

**Expected result:** A list including `('path_test_1', 'WATCH')`.

**Why this step matters:** You have verified that the database accepts writes, that the path schema is correct (state in allowed values), and that the file is separate from production.

5. Understand what happens next (not executed here — documented, not fabricated).

- To log interactions: use `interactions` table (interaction_type, direction, path_id, evidence references).
- To record evidence: use `evidence` table (source paths, quotes, timestamps, provenance).
- To check readiness: use `cli_readiness` (reports lowest unmet item from a checklist; qualifying questions trigger 72-hour follow-up).
- To watch a page: watch pipeline produces events/diffs when changed; zero writes when unchanged.
- To guard an action: `guard_check` evaluates authorization; denied actions do not occur.
- To prepare an outbox draft: `outbox_drafts` records the proposal; no send without authorization (`act=OFF`).

These are described in source and documentation, not invented for this guide.

**What success looks like:** The disposable database contains your synthetic record, production is untouched, no upstream message was sent, and the CLI reads from the correct database.

---

## How to understand the results

**What this system produces:**

- **Database records:** paths, mentors, interactions, evidence, event_store, budget, hours_log, outbox_drafts, kill_state, approval_tokens, readiness, ranking outputs.
- **CLI outputs:** help messages, read-only inspection results, readiness reports with lowest unmet item, audit findings (critic-only), ranking results (with sort-aid label, no universal score).
- **Reports:** `docs/PHASE_9_*.md` (status, evidence, blocker ledger); `docs/P7_FINAL_ACCEPTANCE.md` (security); `README.md` (current status matrix).
- **Files:** `tmp/` disposable tests; `data/agentos.sqlite` (production — do not edit directly); `migrations/` history; `config/` settings.

**Distinguishing results:**

- **No record found:** The query returned nothing (e.g., no evidence linked to a claim). This is not proof of absence; it is proof that the evidence was not recorded.
- **Record exists but incomplete:** A path exists but prerequisites or evidence links are missing. Readiness reports this.
- **Insufficient evidence:** The system's evidence ledger has fewer links than the claim requires. The auditor reports this explicitly.
- **Explicit negative (verified):** The guard denied an action because authorization was missing. The denial is logged; the action did not occur.
- **Blocked (evaluation):** A benchmark or evaluator requires real data or owner input that is not present. The status is `BLOCKED`; it is not `PASS`, not `FAIL`, not `UNKNOWN` by omission.
- **Deferred:** The subsystem trigger has not been met. It is not started, not hidden.

**Where to inspect state:**

- Database: use `sqlite3 data/agentos.sqlite` (read-only) or your disposable file; verify with `sqlite_master`, `PRAGMA integrity_check`.
- Migration status: inspect `sqlite_master` table names; compare to V002/V012 documentation.
- Evidence: `evidence` table (id, path_id, source_path, quote, timestamp, provenance).
- Readiness: `readiness` / `cli_readiness` output (lowest unmet item listed first).
- Status records: the canonical matrix (`docs/PHASE_9_CANONICAL_STATUS_MATRIX.md`) and blocker ledger (`docs/PHASE_9_BLOCKER_LEDGER.md`).

---

## How to inspect state

**Purpose:** See what the system knows, without performing unauthorized actions.

**Before you start:** Confirm which database file is active (`AGENTOS_DB_PATH`).

**Steps:**

1. Read-only SQL inspection (safe; does not change state):

```powershell
sqlite3 tmp/guide_disposable.sqlite "SELECT id, state FROM paths LIMIT 5;"
```

**Expected result:** Rows from your synthetic records or from production if you used production file. Read-only SELECT does not modify the database.

2. Check schema (shows what tables exist):

```powershell
sqlite3 tmp/guide_disposable.sqlite ".schema"
```

3. Check integrity (safe; read-only check):

```powershell
sqlite3 tmp/guide_disposable.sqlite "PRAGMA integrity_check;"
```

**Expected result:** `ok`. If it is not `ok`, do not proceed with writes until the cause is found (see [Troubleshooting](#common-errors-and-fixes)).

4. Inspect migration-related tables (shows whether migrations applied):

```powershell
sqlite3 tmp/guide_disposable.sqlite "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
```

**Expected result:** Names matching V002–V010 schema (e.g., `paths`, `mentors`, `interactions`, `evidence`, `event_store`, `budget`, `hours_log`, `approval_tokens`, etc.).

---

## How to run tests

**Purpose:** Verify behavior. Understand which checks pass and which remain documented as not completed.

**Before you start:** Project installed; `uv` available; database not required for most unit tests (some integration tests may need a disposable DB).

**Important distinction:** A passing test proves only the behavior that test covers. It does not prove that the full application is ready, that benchmarks pass, or that real-data evaluations are complete. This guide does not claim a full suite pass because historical failures exist (`tests/unit/test_level5_watcher_pipeline.py`; `tests/unit/test_p7d_rate_regression.py`; `tests/unit/test_p7e_provenance_synthetic.py`) and some evaluations are blocked by missing external inputs.

**Steps:**

1. Focused verified test (auditor domain — P9-2 verified):

```powershell
uv run pytest tests/test_auditor_domain.py -q
```

**What this checks:** 15 auditor-related tests (claim evidence, partial, no support, contradicted, stale, assumption, deliverable, mentor, exceeds, empty, malformed, irrelevant, hostile, rewrite, adversarial). It does not test evidence retrieval from real proposal inputs.

**Safety:** This does not change the production database. It uses test fixtures.

**Expected result:** 15 collected; exit 0 (if executed; not all were executed in this session's verification — check your own run).

2. Guard / authorization test (P9-3 verified; E702 syntax documented at 35/48):

```powershell
uv run pytest tests/unit/test_guard.py -q
```

**Note:** This file has E702 (multiple statements on one line) at lines 35 and 48. The logic is unchanged; fix is safe (split the semicolon line). Do not suppress this by disabling rules — fix it.

3. Budget / hours (verified implementations):

```powershell
uv run pytest tests/test_level7_budget_engine.py -q
uv run pytest tests/test_level7_hours_cli.py -q
```

4. Integration (disposable DB safe; verifies actual repository paths and evidence):

```powershell
uv run pytest tests/test_level2_3_integration.py -q
```

**What it checks:** Path/repo/evidence/readiness integration using real modules.

**Note:** It requires a working SQLite setup. It does not invent production evidence.

5. Review status of other tests before claiming full acceptance:
- `tests/unit/test_level5_watcher_pipeline.py`: has 2 reported historical failures (changed/unchanged event/diff).
- `tests/unit/test_p7d_rate_regression.py`: 1 reported failure.
- `tests/unit/test_p7e_provenance_synthetic.py`: 2 reported failures.

See `docs/PHASE_9_REGRESSION_REPORT.md` for the evidence on these.

---

## How to understand security and limitations

**Before you continue:** If you are new, read this section before performing any action that might affect persistent state or authorization.

**What the system protects:**

- Your data stays in the local SQLite file you configure (`AGENTOS_DB_PATH`). It does not go to a remote service automatically.
- The `Guard` denies actions that are not permitted (e.g., unauthorized Outbox drafts). It fails closed (denies if authorization is missing).
- The `kill_state` can stop actions at an epoch.
- The `approval_tokens` bind authorization to a specific target/state/time.
- The `budget` and `hours` enforce rolling 30-day limits.
- `act=OFF` means no command will post to GitHub, send a message, create a PR comment, or perform any upstream effect — even if the code supports the operation structurally.

**What the current implementation does not protect (limitations — not hidden):**

- The benchmark evaluation (L9/L11) requires 50 genuinely sourced and labeled issues — the code cannot fabricate those. The benchmark is **blocked**, not failed by code.
- The quiz/reviewer evaluator (L10/L12) requires a second genuine owner labelling session with at least 7 days between sessions, and evaluator metrics from real labels. The implementation exists; the evaluation is **blocked** by missing owner input.
- The proposal auditor real-data E2E (L16 Design A) requires a proposal draft, verified idea-page URL/content, programme-hours log, and linked evidence — all currently absent (DB `evidence=0` preserved from P8). The implementation is verified; the evaluation is **blocked**.
- The Sandbox (L14) exists but full acceptance requires a verified trigger and resolved amendment scope — neither is currently satisfied. Existing work is preserved, not expanded.
- The Context Engine (L13) and PR Shepherd (L15) are deferred (not triggered; not needed as bottlenecks).
- Design B is deferred.

**What you should never do:**

- Do not disable `act=OFF` to “make the workflow work.” The workflow that requires upstream posting requires authorization and approval, not just a flag change.
- Do not invent benchmark labels or evaluation answers to make a test appear complete.
- Do not edit historical G1 records or baseline records to claim a pass.
- Do not delete the production database to “reset” — use a disposable file for testing.
- Do not assume a passing syntax test proves full readiness.

---

## Common errors and fixes

Use this table only for verified conditions. If your situation does not match, collect the error message and the file/line where it occurred before changing anything.

| Symptom | Meaning | Checks | Safe next action |
|---|---|---|---|
| `python --version` missing / wrong | Python not installed or not in PATH | Check `python --version`; check install path | Install Python 3.12+ per python.org; do not change project code |
| `uv --version` missing | Package manager not installed | Check `uv --version` | Install `uv`; do not edit dependencies |
| `ERROR: Set AGENTOS_DB_PATH or DATABASE_URL` | Database path not configured; `cli_path` requires it | Check `echo $env:AGENTOS_DB_PATH`; check `data/agentos.sqlite` exists | Set variable; or rely on default file; do not invent a file |
| `sqlite3` connection failure (file missing / permission) | DB file missing or locked | Check file path; check `sqlite3 $env:AGENTOS_DB_PATH ".tables"` | Use disposable file for testing; preserve production |
| `sqlite3`: no tables in disposable file | Migrations not applied | Check `sqlite_master`; apply `run(DatabaseConfig.from_env())` | Apply migrations; verify with `PRAGMA integrity_check` |
| `sqlite3`: integrity_check not ok | Database corruption or partial migration | Check which migrations applied; check for write interruption | Do not edit DB directly; use backup; consult `docs/PHASE_9_MIGRATION_RECOVERY_LOG.md` |
| `pytest` collection error | Syntax error or import error in test/file | Check error message; check file that failed | Fix syntax (e.g., E702); do not suppress rules globally |
| `pytest` failure (test_level5/7/p7d/p7e) | Historical failure recorded | Check `docs/PHASE_9_REGRESSION_REPORT.md`; check source test | Preserve failure; do not weaken assertion; fix root cause only |
| `ruff` / `mypy` error (e.g., E702, import) | Style or type error | Check file/line from message | Fix locally; do not disable rules for unrelated files |
| CLI command not recognized (`agentos`) | Package not installed / not in path | Check `pyproject.toml` scripts; check `.venv/`; run `uv sync` | Install; do not invent command |
| Operation denied by Guard | Authorization missing or kill epoch reached | Check `approval_tokens`; check `kill_state`; check `Guard` logic | Request authorization through proper path; do not disable Guard |
| Outbox draft not sending | `act=OFF`; authorization missing | Check `act=OFF`; check `approval_tokens` | Do not switch `act` to enable; get authorization through proper path |
| Readiness missing / lowest unmet unclear | Evidence or prerequisites missing | Check `cli_readiness`; check `readiness` table; check evidence links | Add real evidence; do not invent readiness |
| Evidence link broken / missing | Source file moved; quote incorrect; provenance missing | Check `evidence` table; check `source_path`; verify with `read` | Correct evidence; do not invent source |
| Benchmark / evaluation claims unavailable | External dataset / owner input / labels missing | Check `docs/PHASE_9_CANONICAL_STATUS_MATRIX.md`; check blocker ledger | Do not substitute synthetic; document BLOCKED with exact prerequisite |
| “Feature listed in plan but not usable” | Implementation exists but evaluation / external input blocked | Check matrix; check `docs/LEVEL_11_*.md`; check `AGENTS.md` §4/§13 | Understand the distinction between implemented and accepted; see matrix |

---

## How to stop safely

**Purpose:** End the session without losing data or weakening controls.

**Before you stop:** Confirm that any in-progress work is saved (database writes are automatic; no separate “save” is needed for SQLite writes unless you changed a file and did not save it — but SQLite commits on each transaction).

**Steps:**

1. Confirm no upstream action was triggered accidentally. (With `act=OFF`, this is the default — no action should have occurred. If you did authorize something through the Outbox, confirm it was intentional.)

2. Stop any background process you started (if any). The CLI itself does not start long-running servers in the basic workflow.

**What happens:** The SQLite file retains all committed writes. The `.env` configuration remains. Nothing is cleaned automatically. The working tree (your documentation changes, if any) remains.

**Safety note:** Do not delete `data/agentos.sqlite` or reset migrations to “clean up.” If you need a clean state, create a disposable file (`tmp/clean.sqlite`) and apply migrations to it. Preserve the production file.

---

## How to restart

**Purpose:** Resume work with the same state.

**Before you restart:** Confirm which database file is active (check `AGENTS_DB_PATH` or the default path). Confirm that no unauthorized upstream effect was triggered (with `act=OFF`, none should be).

**Steps:**

1. Open a terminal in the project directory.
2. Confirm `AGENTS_DB_PATH` if you use a non-default file.
3. Confirm database readability: `sqlite3 $env:AGENTS_DB_PATH ".tables"`
4. Start the CLI or inspect state as needed.

**What to expect:** The system reads from the same SQLite file. Previous records are preserved. No automatic “re-initialization” occurs unless you run the migration runner again (which applies only missing migrations).

---

## How to reset cleanly only when safe

**Purpose:** Create a fresh isolated state for a specific test.

**When this is safe:** Only when you are using a disposable file (not `data/agentos.sqlite`) and you have a copy of the production file if needed.

**Before you start:** Confirm that the file you will change is not the production file.

**Steps:**

1. Confirm the file name.

```powershell
Write-Host "Your disposable DB: $env:AGENTOS_DB_PATH"
```

2. Create a new disposable file.

```powershell
New-Item -ItemType File -Path tmp/fresh.sqlite
```

3. Set environment.

```powershell
$env:AGENTOS_DB_PATH = "tmp/fresh.sqlite"
```

4. Apply migrations.

```powershell
uv run python -c "from agentos.db.config import DatabaseConfig; from agentos.db.migrations import run; import os; os.environ['AGENTOS_DB_PATH']='tmp/fresh.sqlite'; run(DatabaseConfig.from_env())"
```

5. Verify.

```powershell
python -c "import sqlite3; c=sqlite3.connect('tmp/fresh.sqlite'); print('integrity=', c.execute('PRAGMA integrity_check').fetchone()[0]); print('tables=', len(c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()))"
```

**Safety note:** Do not delete the production file (`data/agentos.sqlite`) to “reset.” Always use a new file name.

---

## Security boundaries

**Before you rely on these controls:** Understand that they are implemented in code and verified by existing tests — but some external audits (live endpoint, full benchmark, full evaluator) remain blocked by missing inputs, per `AGENTS.md` and `docs/P7_FINAL_ACCEPTANCE.md`.

**What is enforced by the code:**

- `act=OFF` prevents outward action by default. The CLI helps, the services read from SQLite, the Guard evaluates authorization, and the Outbox holds drafts. No command sends a message without authorization.
- Guard denial rules are deterministic. The `test_guard.py` verifies denial conditions.
- Approval tokens bind to a target/state/time. Stale or unauthorized actions are rejected.
- Kill epoch stops actions at a defined point.
- Budget uses rolling 30-day (not calendar-month) rules.
- Secret scanning: `.env` excluded; no secrets in source or new documentation.
- Provenance: `evidence` links to file/line; `source_path` preserved; no inference of personal attributes.
- People-data restriction: public role only; no speculative profiles; evidence from owner's own logged interactions.

**What is not verified or requires external authorization:**

- Benchmark evaluation (L9/L11) — requires 50 genuinely sourced and labeled issues.
- Evaluator acceptance (L10/L12) — requires genuine owner labeling session + 7-day verification.
- Real-data proposal audit (L16) — requires real proposal content + idea page + hours + evidence links.
- Full Sandbox acceptance (L14) — requires trigger + amendment resolution.
- Live external endpoint audit — preserved separately; `act=OFF` is the enforced boundary.

**What to do:** Use the system within its verified scope. Do not disable controls to make an unverified workflow succeed. Document missing evidence rather than substituting synthetic data.

---

## Glossary

**CLI:** Command-Line Interface — the text commands you type into a terminal to control the application.

**SQLite:** A database that stores information in a local file (not a separate server). This project uses it.

**Migration:** A controlled change to the database structure, applied in a recorded order (V001, V002, ...).

**Virtual environment:** A separate folder (`.venv/`) that holds a project's Python packages so they do not mix with other projects.

**Provenance:** A record of where information came from, when it was obtained, and how.

**Evidence:** A structured link from a claim to a source (file, line, quote, timestamp).

**Acceptance (implementation vs evaluation):** Implementation = the code exists and passes relevant tests. Evaluation = the required external evidence (benchmark labels, owner labels, proposal inputs) was verified by a genuine process.

**Guard:** The authorization control that denies unauthorized actions and fails closed.

**Outbox:** The draft-storage mechanism for proposed upstream actions; sends only after authorization.

**Kill epoch:** A defined point after which the system stops further action for a given target.

**Status labels (used in this guide and in the matrix):**
- `ACCEPTED` — implementation verified and evaluation completed (where required).
- `BLOCKED` — a specific external prerequisite (data, authorization, dataset) is missing.
- `DEFERRED` — conditional subsystem; trigger not met; not started.
- `FAIL` — historical evaluation result (preserved, not rewritten).
- `NOT_VERIFIED` — check not performed or insufficient evidence.
- `PASS` — only used when a specific command/test/result was actually verified.

---

## Where to go next

If you have completed the quick start and understand the safety boundaries:

- To inspect the current status of every component: [`docs/PHASE_9_CANONICAL_STATUS_MATRIX.md`](docs/PHASE_9_CANONICAL_STATUS_MATRIX.md)
- To understand Phase 9 hardening evidence: [`docs/PHASE_9_FINAL_ACCEPTANCE.md`](docs/PHASE_9_FINAL_ACCEPTANCE.md)
- To see the blocker ledger (B-01 through B-06): [`docs/PHASE_9_BLOCKER_LEDGER.md`](docs/PHASE_9_BLOCKER_LEDGER.md)
- To read the security and cross-cutting report: [`docs/P7_FINAL_ACCEPTANCE.md`](docs/P7_FINAL_ACCEPTANCE.md) · [`docs/P7_CROSS_CUTTING_SECURITY_REPORT.md`](docs/P7_CROSS_CUTTING_SECURITY_REPORT.md)
- To understand the proposal auditor scope and current E2E state: [`docs/PHASE_8_FINAL_ACCEPTANCE.md`](docs/PHASE_8_FINAL_ACCEPTANCE.md) · [`docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md`](docs/PROPOSAL_EVIDENCE_AUDITOR_SCOPE.md)
- To see the account of what was authorized despite G1: [`docs/G1_OVERRIDE_AUTHORIZED.md`](docs/G1_OVERRIDE_AUTHORIZED.md)
- To inspect commands and architecture: [`README.md`](README.md) · [`AGENTS.md`](AGENTS.md)
- To find source code for a component: [`src/agentos/`](src/agentos/) (organized by CLI, db/config, core services, readiness, ranking, audit, watch, kill)
- To find tests: [`tests/`](tests/) — unit (`tests/unit/`) and integration (`tests/integration/`)
- To find the migration and database history: [`migrations/`](migrations/) · [`sql_migrations/`](sql_migrations/) · [`src/agentos/db/sqlite_migrations/`](src/agentos/db/sqlite_migrations/)
- To check the actual environment setup: `.env.example` · `pyproject.toml` · `uv.lock`

**Final reminder:** This guide teaches the verified portion of the system. It explains what is blocked, deferred, or requiring external input. It does not ask you to invent data, disable safety controls, or claim a benchmark result that does not have real labels. If a result is uncertain, inspect the evidence (database, reports, source) rather than assuming success.

*Guide version: aligned with v2.1, Phase 9 hardening (P9-1 through P9-7 completed), and the verified repository state at 2026-10-14.*
