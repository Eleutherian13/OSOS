"""Architectural contract tests for Level 0.

These enforce the Level 0 scope boundaries: implementation code contains no
provider SDKs or future-level machinery, importing/starting the package never
touches the network, and the repository contains no secrets.

Only implementation code (src/) is scanned for prohibited features; tests and
documentation may mention the terms.
"""

import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import agentos

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = Path(agentos.__file__).resolve().parent
DB_PACKAGE = PACKAGE_DIR / "db"


def _is_db_module(path: Path) -> bool:
    return path.resolve().is_relative_to(DB_PACKAGE)


PROHIBITED_TERMS = (
    "OpenAI",
    "Anthropic",
    "Ollama",
    "LangChain",
    "LangGraph",
    "LiteLLM",
    "pgvector",
    "Redis",
    "Temporal",
    "Celery",
    "Streamlit",
    "RAG",
    "embedding",
    "GitHub",
    "worker",
    "queue",
    "sandbox",
    "sqlalchemy",
    "alembic",
)
"""Prohibited features everywhere, including the database package.

The only permitted database driver is ``psycopg`` which is scoped to
``src/agentos/db/``. Any ``psycopg`` reference outside that package breaks
the level-1 boundary.
"""
PSYCGPSCOPED_ALLOWED = {"psycopg"}

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?:postgres(?:ql)?|mysql)://[^\s:@/]+:[^\s@]+@"),
)

_SKIP_DIRS = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    ".kilo",
}


def _implementation_files() -> Iterator[Path]:
    """Yield the Python implementation files of the agentos package."""
    yield from sorted(PACKAGE_DIR.rglob("*.py"))


def _repo_files() -> Iterator[Path]:
    """Yield project files, skipping VCS, virtualenv, cache, and local-env files."""
    for path in PROJECT_ROOT.rglob("*"):
        rel = path.relative_to(PROJECT_ROOT).parts
        if any(part in _SKIP_DIRS for part in rel):
            continue
        if path.is_file() and path.name != ".env":
            yield path


def test_implementation_code_has_no_prohibited_features() -> None:
    """No Level 0 module may reference future-level machinery or provider SDKs.
    The database package (db/) is permitted only the psycopg driver."""
    for path in _implementation_files():
        text = path.read_text(encoding="utf-8")
        for term in PROHIBITED_TERMS:
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            match = pattern.search(text)
            assert match is None, f"{path.name} mentions prohibited feature {term!r}"
    # db/ package permitted only psycopg — anything else in db/ is a defect.
    for path in DB_PACKAGE.rglob("*.py") if DB_PACKAGE.exists() else []:
        text = path.read_text(encoding="utf-8")
        for term in ("sqlalchemy", "alembic", "OpenAI", "Anthropic", "Ollama", "LangChain", "LangGraph", "Redis", "Temporal", "Celery", "Streamlit", "pgvector", "embedding"):
            match = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE).search(text)
            assert match is None, f"db/{path.name} mentions forbidden feature {term!r}"


def test_import_never_accesses_the_network() -> None:
    """Importing and wiring the CLI must not open sockets."""
    code = "\n".join(
        [
            "import socket",
            "def _no_network(*args, **kwargs):",
            "    raise AssertionError('network access during startup')",
            "socket.socket = _no_network",
            "socket.create_connection = _no_network",
            "import agentos",
            "import agentos.cli",
        ]
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr


def test_repository_contains_no_secrets() -> None:
    """No tracked-shape project file may contain secret-shaped strings."""
    for path in _repo_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            assert match is None, f"{path} matches secret pattern {pattern.pattern!r}"
