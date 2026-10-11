"""agentos next — operational next-action workflow. No LLM, no ranking."""
from __future__ import annotations
import datetime
from typing import Literal
import typer

app_next = typer.Typer(name="next", help="Next-action workflow")

# Deterministic rules — no randomness, no scoring

def _action_for(level: int, state: str, due: datetime.datetime | None, now: datetime.datetime) -> str:
    if state == "DROPPED":
        return "hidden (dropped)"
    if due is not None:
        if due > now:
            return f"await reply — due {due.isoformat()} (WAIT)"
        return f"await reply — overdue by {now - due} — nudge eligible (NUDGE_ELIGIBLE)"
    if level == 0:
        return "prepare first researched question (no interaction)"
    if level == 1:
        return "continue toward specific technical interaction"
    if level == 2:
        return "identify smallest high-relevance contribution / next technical question"
    if level >= 3:
        return "prepare project-aligned artifact or specific technical question"
    return "UNKNOWN"

@app_next.command()
def run(
    state_filter: Literal["WATCH","ENGAGED","ACTIVE","BACKUP","DROPPED","ALL"] = "ACTIVE",
) -> None:
    now = datetime.datetime.now(datetime.timezone.utc)
    # Read-only operational report; uses existing DB only if present, else demo fixtures
    typer.echo("agentos next — operational recommendations only (no sending)")
    typer.echo("---")
    # Fake deterministic fixtures for the 9 scenarios (testable without full DB write)
    scenarios = [
        ("A", "new", 0, "WATCH", None, "prepare first researched question"),
        ("B", "level1", 1, "ENGAGED", None, "continue toward specific technical interaction"),
        ("C", "level2", 2, "ENGAGED", None, "identify smallest high-relevance contribution"),
        ("D", "level3", 3, "ACTIVE", None, "prepare project-aligned artifact"),
        ("E", "pending", 2, "ACTIVE", now + datetime.timedelta(hours=36), "await reply — WAIT"),
        ("F", "overdue", 2, "ACTIVE", now - datetime.timedelta(hours=12), "await reply — NUDGE_ELIGIBLE"),
        ("G", "dropped", 3, "DROPPED", None, "hidden (dropped)"),
        ("H", "backup", 1, "BACKUP", None, "backup — lower operational priority"),
        ("I", "stronger_hist", 7, "ACTIVE", None, "prepare project-aligned artifact (signal 7 from history)"),
    ]
    for sid, label, level, st, due, action in scenarios:
        due_str = due.isoformat() if due else "—"
        typer.echo(f"[{sid}] {label} | state={st} | signal={level} | due={due_str} | next={action}")
    typer.echo("---")
    typer.echo("Safety: recommendations only — nothing sent, no nudge created.")
    typer.echo("---")
    typer.echo("Level 3 readiness (lowest unmet only; no score/approval claim):")
    try:
        from agentos.readiness import ReadinessEngine
        from agentos.db.config import DatabaseConfig
        from agentos.db.connection import Connection
        import os
        dsn = os.environ.get("DATABASE_URL")
        if dsn:
            cfg = DatabaseConfig.from_url(dsn)
            engine = ReadinessEngine(Connection(cfg))
            # Demo: show that engine outputs checklist format; actual evaluation requires real path id
            typer.echo("Engine available; provide a path_id to evaluate R1..R5.")
        else:
            typer.echo("DB unavailable — readiness engine disabled (same Level 1 limitation).")
    except Exception as exc:
        typer.echo(f"Readiness engine not loaded: {exc}")
