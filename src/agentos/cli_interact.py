"""Interaction loop: add interaction with ladder validation + follow-up."""
import typer
from agentos.domain.errors import ValidationError

app_interact = typer.Typer(name="interact", help="Interaction commands")

@app_interact.command()
def add(
    path: str,
    level: int,
    link: str,
    direction: str = "outbound",
    quote: str | None = None,
    note: str | None = None,
):
    if level < 0 or level > 7:
        raise typer.BadParameter("level must be 0-7")
    if not link:
        raise typer.BadParameter("link is required")
    if level >= 5 and not quote:
        raise typer.BadParameter("quote required for level >= 5")
    typer.echo(f"interaction {level} on {path}: {link}")
    if direction == "outbound":
        typer.echo("follow-up due in 72h")
