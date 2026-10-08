# OSS-AgentOS

OSS-AgentOS is an incremental system for managing open-source contribution
paths — and, in later levels, for assisting with research, contribution work,
evidence collection, and policy handling.

The system is deliberately built in **levels**. Each level is small, complete,
and verified on its own, so later levels extend the foundation without
architectural rewrites.

## Development philosophy

- **Small complete levels.** Every level installs, runs, and passes its own
  gates. Nothing is half-wired.
- **Boundaries before features.** Architectural contracts are written down and
  enforced by tests before the features that depend on them exist.
- **Dependency discipline.** A dependency is added only when code actually
  uses it. Nothing is installed "for later".
- **No secrets in code.** Configuration and credentials come from the
  environment, never from the repository.

## Level 0 — software foundation

Level 0 is **only** the software foundation. It provides:

- a Python 3.12 project managed with [uv](https://docs.astral.sh/uv/)
- a `src`-layout package `agentos` with a minimal [Typer](https://typer.tiangolo.com/) CLI
- [Pydantic v2](https://docs.pydantic.dev/) available as the base modeling layer
- pytest, ruff, and mypy wired up and passing
- documentation of the level's scope and the future LLM runtime contract

It contains **no domain logic, no database, and no LLM integration**.

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```
uv sync
```

This creates the virtual environment, installs Python 3.12 if it is missing
(uv manages the interpreter via `.python-version`), and installs the project
editable together with its dev dependencies.

## CLI usage

```
uv run agentos --help
uv run agentos version
```

The CLI starts quickly, imports cleanly, makes no network requests, requires
no database and no API keys, and performs no background work. These properties
are enforced by the test suite (`tests/test_contract.py`).

## Development commands

| Command | What it does |
| --- | --- |
| `uv run pytest` | run the test suite |
| `uv run ruff check .` | lint |
| `uv run mypy .` | type check (strict) |
| `uv sync` | (re)install the environment reproducibly (`uv sync --frozen` uses the lockfile) |

With `make` installed, `make install`, `make test`, `make lint`,
`make typecheck`, and `make check` run the same steps through uv.

## Current limitations

- No database access, no persistence, no PostgreSQL connection or schema.
- No LLM runtime of any kind — no fake, local, or paid provider adapter
  (the contract for those is documented, not implemented: see
  `docs/LLM_RUNTIME_CONTRACT.md`).
- No GitHub integration, no automation, no workers or queues.
- `config/`, `registry/`, `migrations/`, and `evals/` are empty placeholders
  reserved for later levels.

## What is intentionally NOT implemented

Level 0 must stay small. The following are explicitly out of scope and are
only allowed to appear in documentation, never in code:

database connections or schemas, migrations with application domain tables,
events / event sourcing, domain entities (projects, mentors, organizations,
interactions, evidence, readiness, watcher, policy registry or evaluator,
Guard, Outbox, approval tokens, kill switch, budget enforcement), GitHub
clients or integrations, Issue Hunter, PR Shepherd, context engine, RAG,
embeddings, vector databases, LLM execution, LLM provider adapters, Ollama /
OpenAI / Anthropic SDKs, LangChain / LangGraph, Redis, Temporal, Celery,
workers, queues, sandboxes, Streamlit dashboards, and any autonomous coding
agent.

The full scope boundary and acceptance criteria live in `docs/LEVEL_0.md`.
