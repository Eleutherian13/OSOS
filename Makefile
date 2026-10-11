# OSS-AgentOS — Level 0 targets. Everything runs through uv.
# If `make` is not installed (common on Windows), run the underlying
# `uv ...` commands directly; they are listed in README.md.

.PHONY: install test lint typecheck check db/migrate db/check db/reset

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

check: lint typecheck test

db/migrate:
	uv run python -c "from agentos.db.config import DatabaseConfig; from agentos.db.migrations import run; import os; cfg=DatabaseConfig.from_env(); run(cfg)"

db/check:
	uv run python -c "from agentos.db.config import DatabaseConfig; from agentos.db.health import is_healthy; import os; cfg=DatabaseConfig.from_env(); print(is_healthy(cfg))"

db/reset:
	@echo "Reset requires a running PostgreSQL; see docs/LEVEL_1.md"
