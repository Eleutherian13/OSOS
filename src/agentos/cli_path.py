"""CLI: agentos path add / show / state"""
import typer
from agentos.domain.errors import ValidationError

app_path = typer.Typer(name="path", help="Path commands")

@app_path.command()
def add(org: str, project: str, state: str = "WATCH"):
    if state not in {"WATCH","ENGAGED","ACTIVE","BACKUP","DROPPED"}:
        raise typer.BadParameter(f"invalid state: {state}")
    typer.echo(f"path created: org={org} proj={project} state={state}")

@app_path.command()
def show(path_id: str):
    typer.echo(f"path={path_id}")

@app_path.command()
def mentor_remove(path_id: str, mentor_id: str):
    typer.echo(f"mentor removed: path={path_id} mentor={mentor_id}")

@app_path.command()
def state(path_id: str, new_state: str):
    if new_state not in {"WATCH","ENGAGED","ACTIVE","BACKUP","DROPPED"}:
        raise typer.BadParameter(f"invalid state: {new_state}")
    typer.echo(f"state changed: {path_id} -> {new_state}")
