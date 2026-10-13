"""CLI: agentos path add / show / state + agentos interact add."""
import typer
import uuid
from datetime import datetime, timezone
from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection
from agentos.db.path_repo import PathMentorRepo, PathRepo, InteractionRepo
from agentos.domain.path_models import Path, Interaction, Followup, PathState, InteractionLevel


app_path = typer.Typer(name="path", help="Path commands")
app_interact = typer.Typer(name="interact", help="Interaction commands")


@app_path.command("add")
def path_add(
    org: str = typer.Option(..., "--org", help="Organization slug"),
    project: str = typer.Option(..., "--project", help="Project slug"),
    path_type: str = typer.Option("other", "--type", help="Path type: gsoc, lfx, or other"),
    state: str = typer.Option("WATCH", "--state", help="Initial state: WATCH, ENGAGED, ACTIVE, BACKUP, DROPPED"),
):
    """Create a new mentor project path."""
    if state not in {"WATCH", "ENGAGED", "ACTIVE", "BACKUP", "DROPPED"}:
        raise typer.BadParameter(f"invalid state: {state}. Must be one of WATCH, ENGAGED, ACTIVE, BACKUP, DROPPED")
    
    import os
    dsn = os.environ.get("AGENTOS_DB_PATH") or os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: Set AGENTOS_DB_PATH or DATABASE_URL", err=True)
        raise typer.Exit(1)
    
    cfg = DatabaseConfig.from_env()
    conn = Connection(cfg)
    repo = PathRepo(conn)
    
    path_id = uuid.uuid4()
    path = Path(
        id=path_id,
        org_id=uuid.uuid4(),  # In real impl, would lookup org by slug
        project_id=uuid.uuid4(),  # In real impl, would lookup project
        path_type=path_type,
        path_slug=f"{org}/{project}",
        state=PathState(state),
    )
    saved = repo.add(path)
    typer.echo(f"Path created: {saved.id} (org={org}, project={project}, state={saved.state.value})")


@app_path.command("show")
def path_show(path_id: str = typer.Argument(..., help="Path ID (UUID)")):
    """Show path details."""
    try:
        pid = uuid.UUID(path_id)
    except ValueError:
        typer.echo("ERROR: Invalid path ID (must be UUID)", err=True)
        raise typer.Exit(1)
    
    import os
    dsn = os.environ.get("AGENTOS_DB_PATH") or os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: Set AGENTOS_DB_PATH or DATABASE_URL", err=True)
        raise typer.Exit(1)
    
    cfg = DatabaseConfig.from_env()
    conn = Connection(cfg)
    repo = PathRepo(conn)
    
    path = repo.get(pid)
    if not path:
        typer.echo(f"Path not found: {path_id}", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"path_id={path.id}")
    typer.echo(f"state={path.state.value}")
    typer.echo(f"path_type={path.path_type}")
    typer.echo(f"path_slug={path.path_slug}")
    typer.echo(f"created_at={path.created_at}")
    typer.echo(f"updated_at={path.updated_at}")


@app_path.command("state")
def path_state(path_id: str = typer.Argument(...), new_state: str = typer.Argument(...)):
    """Change path state."""
    if new_state not in {"WATCH", "ENGAGED", "ACTIVE", "BACKUP", "DROPPED"}:
        raise typer.BadParameter(f"invalid state: {new_state}")
    
    try:
        pid = uuid.UUID(path_id)
    except ValueError:
        typer.echo("ERROR: Invalid path ID", err=True)
        raise typer.Exit(1)
    
    import os
    dsn = os.environ.get("AGENTOS_DB_PATH") or os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: Set AGENTOS_DB_PATH or DATABASE_URL", err=True)
        raise typer.Exit(1)
    
    cfg = DatabaseConfig.from_env()
    conn = Connection(cfg)
    repo = PathRepo(conn)
    
    path = repo.get(pid)
    if not path:
        typer.echo(f"Path not found: {path_id}", err=True)
        raise typer.Exit(1)
    
    new = PathState(new_state)
    updated = repo.transition(pid, new)
    if updated:
        typer.echo(f"State changed: {path_id} {path.state.value} -> {updated.state.value}")
    else:
        typer.echo(f"Invalid transition: {path.state.value} -> {new_state}", err=True)
        raise typer.Exit(1)


@app_path.command("mentor-remove")
def mentor_remove(
    path_id: str = typer.Argument(..., help="Path ID (UUID)"),
    mentor_id: str = typer.Argument(..., help="Mentor ID (UUID)"),
) -> None:
    """Remove a mentor from a mentor project path."""
    import os
    dsn = os.environ.get("AGENTOS_DB_PATH") or os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: Set AGENTOS_DB_PATH or DATABASE_URL", err=True)
        raise typer.Exit(1)
    try:
        pid = uuid.UUID(path_id)
        mid = uuid.UUID(mentor_id)
    except ValueError:
        typer.echo("ERROR: path_id and mentor_id must be UUIDs", err=True)
        raise typer.Exit(1)
    cfg = DatabaseConfig.from_env()
    conn = Connection(cfg)
    repo = PathMentorRepo(conn)  # import at module level below
    removed = repo.remove(pid, mid)
    if removed:
        typer.echo(f"Mentor removed: {mentor_id} from path {path_id}")
    else:
        typer.echo(f"No association found: mentor {mentor_id} not linked to path {path_id}")


@app_interact.command("add")
def interact_add(
    path_id: str = typer.Option(..., "--path", help="Path ID"),
    interaction_type: str = typer.Option(..., "--type", help="Type: email, issue, pr, meeting, other"),
    direction: str = typer.Option(..., "--direction", help="Direction: inbound, outbound, mutual"),
    level: int = typer.Option(..., "--level", help="Level (0-7)"),
    link: str = typer.Option(..., "--link", help="Source link"),
    channel: str = typer.Option("UNKNOWN", "--channel", help="Channel: PUBLIC, PRIVATE, UNKNOWN"),
    quote: str = typer.Option(None, "--quote", help="Quoted text (required for level >= 5)"),
    summary: str = typer.Option(None, "--summary", help="Summary text"),
):
    """Add an interaction record."""
    # Validate level
    if level < 0 or level > 7:
        raise typer.BadParameter("level must be 0-7")
    
    # Validate channel
    if channel not in {"PUBLIC", "PRIVATE", "UNKNOWN"}:
        raise typer.BadParameter("channel must be PUBLIC, PRIVATE, or UNKNOWN")
    
    # Validate direction
    if direction not in {"inbound", "outbound", "mutual"}:
        raise typer.BadParameter("direction must be inbound, outbound, or mutual")
    
    # Validate interaction_type
    if interaction_type not in {"email", "issue", "pr", "meeting", "other"}:
        raise typer.BadParameter("invalid interaction_type")
    
    # Level 5+ requires quote
    if level >= 5 and not quote:
        raise typer.BadParameter("level >= 5 requires --quote")
    
    try:
        pid = uuid.UUID(path_id)
    except ValueError:
        typer.echo("ERROR: Invalid path ID", err=True)
        raise typer.Exit(1)
    
    import os
    dsn = os.environ.get("AGENTOS_DB_PATH") or os.environ.get("DATABASE_URL")
    if not dsn:
        typer.echo("ERROR: Set AGENTOS_DB_PATH or DATABASE_URL", err=True)
        raise typer.Exit(1)
    
    cfg = DatabaseConfig.from_env()
    conn = Connection(cfg)
    inter_repo = InteractionRepo(conn)
    
    # Verify path exists
    from agentos.db.path_repo import PathRepo
    path_repo = PathRepo(conn)
    path = path_repo.get(pid)
    if not path:
        typer.echo(f"Path not found: {path_id}", err=True)
        raise typer.Exit(1)
    
    interaction = Interaction(
        id=uuid.uuid4(),
        path_id=pid,
        interaction_type=interaction_type,
        direction=direction,
        level=level,
        link=link,
        channel=channel,
        quote=quote,
        summary=summary,
    )
    
    # Validate
    errors = interaction.validate()
    if errors:
        for e in errors:
            typer.echo(f"ERROR: {e}", err=True)
        raise typer.Exit(1)
    
    saved = inter_repo.add(interaction)
    typer.echo(f"Interaction added: {saved.id} (path={path_id}, type={interaction_type}, level={level})")
    
    # Auto-create followup for outbound interactions at level >= 2
    if direction == "outbound" and level >= 2:
        from agentos.db.path_repo import FollowupRepo
        followup_repo = FollowupRepo(conn)
        if followup_repo.ensure_no_duplicate(pid, saved.id):
            due = datetime.now(timezone.utc) + __import__('datetime').timedelta(hours=72)
            followup = Followup(
                id=uuid.uuid4(),
                path_id=pid,
                interaction_id=saved.id,
                due_at=due,
                note=f"Follow-up required for outbound interaction at level {level}",
            )
            followup_repo.add(followup)
            typer.echo(f"Followup created: due={due.isoformat()}")


# Register with main app
app_path.add_typer(app_interact, name="interact")
