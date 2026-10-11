"""Kill-switch state (Prompt 3). DB + STOP-file fast path."""
from __future__ import annotations

from pathlib import Path

STOP_FILE = Path("STOP")


def stop_file_present() -> bool:
    return STOP_FILE.exists()


def set_stop_file() -> None:
    STOP_FILE.write_text("AgentOS emergency stop active. Reconcile with DB before resume.\n")
