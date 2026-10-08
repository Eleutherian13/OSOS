# Level 0 — Software Foundation

## Objective

Level 0 establishes the smallest clean, maintainable, reproducible foundation
for OSS-AgentOS. It is not a feature level: it exists so that every later
level can be added without architectural rewrites.

A developer must be able to: install with uv, import the package, run the
CLI, run tests, run ruff, run mypy, and understand the project from the
README — without PostgreSQL, GitHub, an LLM, API credentials, or internet
access (beyond the one-time package download).

## Included functionality

- Python 3.12 project (uv-managed, pinned via `.python-version` and
  `requires-python = ">=3.12,<3.13"`), `uv.lock` committed for
  reproducibility.
- `src`-layout package `agentos` with `__version__`.
- Typer CLI executable `agentos` with `--help`, `--version`, and a
  `version` command. No other commands exist.
- Pydantic v2 available as the shared modeling base.
- pytest test suite: package import, CLI startup/help/version, invalid
  invocation, clean failure behavior, and architectural contract audits.
- ruff and mypy (strict) configured and passing.
- `.env.example` (no variables required in Level 0) and `.gitignore`.
- Makefile with `install`, `test`, `lint`, `typecheck`, `check` (all through
  uv; direct `uv` commands are the documented fallback).
- `docs/LLM_RUNTIME_CONTRACT.md` — documentation-only contract for the
  future FAKE/LOCAL/PAID LLM runtime.
- Empty placeholder directories reserved for later levels: `config/`,
  `registry/`, `migrations/`, `evals/`.

## Excluded functionality (enforced, not just intended)

Level 0 implements none of the following, and `tests/test_contract.py`
mechanically scans implementation code to keep it that way:

- PostgreSQL connection logic, domain schema, or migrations with application
  domain tables.
- Events, event sourcing, and all domain entities: MentorProjectPath,
  organizations, projects, mentors, interactions, evidence, readiness,
  watcher, policy registry logic, policy evaluator, Guard, Outbox, approval
  tokens, kill switch, budget enforcement.
- GitHub clients, Issue Hunter, PR Shepherd, context engine, RAG,
  embeddings, vector databases.
- LLM execution, LLM provider adapters, Ollama client, paid API clients,
  OpenAI SDK, Anthropic SDK, LangChain, LangGraph.
- Redis, Temporal, Celery, workers, queues, sandboxes.
- Streamlit, dashboards, autonomous coding agents.

Documentation mentions are allowed; implementation is not.

## Acceptance criteria

1. `uv sync` succeeds and `uv.lock` is committed; `uv sync --frozen` works.
2. `uv run agentos --help` exits 0 with usage output.
3. `uv run agentos version` exits 0 with the package version.
4. `uv run pytest` (or `pytest -q` in an activated venv) is fully green with
   no PostgreSQL, GitHub, LLM, Ollama, paid API, credentials, or network.
5. `uv run ruff check .` reports no violations; no blanket suppressions.
6. `uv run mypy .` passes in strict mode; no global disables, no `Any` abuse.
7. An unknown CLI command exits non-zero with a clean usage error.
8. Importing `agentos` and `agentos.cli` opens no sockets (audited in a
   subprocess with `socket` sabotaged).
9. No secret-shaped strings anywhere in the repository (audited).
10. Implementation code contains none of the excluded terms (audited).
11. A fresh developer can follow README.md end to end and get the same
    results.

## Next authorized level

Level 1 is expected to introduce the provider-neutral LLM runtime (fake
adapter first) according to `docs/LLM_RUNTIME_CONTRACT.md`, under its own
level prompt. Nothing from Level 1 may leak into Level 0 code.

### Where Level 1 code goes

- A new `src/agentos/db/` package for database operations (when a Level 1
  prompt authorizes a datastore). Do not create it now.
- A new `src/agentos/llm/` package holding the provider-neutral LLM
  interface and the fake/local/paid adapters. Do not create it now.
- A new `src/agentos/policy/` package for policy evaluation (only when
  authorized by a level prompt). Do not create it now.
- Domain entities (projects, mentors, evidence, etc.) live in `src/agentos/`
  packages per their feature, never at package top-level as globals.
- Migrations stay in `migrations/`; never put application domain tables in
  Level 0.
