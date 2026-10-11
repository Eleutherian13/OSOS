"""agentos readiness [path] — deterministic 5-item checklist only."""
import typer, uuid, os
from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection
from agentos.readiness import ReadinessEngine

app_readiness = typer.Typer(name="readiness", help="Readiness checklist R1..R5")

@app_readiness.command()
def check(path_id: str):
    try:
        pid = uuid.UUID(path_id)
    except Exception:
        typer.echo("ERROR: invalid path UUID")
        raise typer.Exit(1)
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: DATABASE_URL not set (PostgreSQL unavailable)")
        raise typer.Exit(1)
    engine = ReadinessEngine(Connection(DatabaseConfig.from_url(dsn)))
    result = engine.evaluate(pid)
    typer.echo(f"Readiness for path {path_id}")
    typer.echo("---")
    for id_ in ["R1","R2","R3","R4","R5"]:
        item = result["items"][id_]
        typer.echo(f"{id_} — {item['description']}: {item['status']}")
        typer.echo(f"   refs: {', '.join(item['refs']) or 'none'}")
        typer.echo(f"   missing: {', '.join(item['missing']) or 'none'}")
    if result.get("all_satisfied"):
        typer.echo("All five recorded readiness requirements are satisfied.")
    else:
        first = result.get("first_unmet")
        if first:
            typer.echo(f"First unmet: {first[0]} — {first[1]} — missing: {', '.join(first[2])}")
