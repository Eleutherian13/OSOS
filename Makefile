# OSS-AgentOS — Level 0 targets. Everything runs through uv.
# If `make` is not installed (common on Windows), run the underlying
# `uv ...` commands directly; they are listed in README.md.

.PHONY: install test lint typecheck check

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

check: lint typecheck test
