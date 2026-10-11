"""Typer CLI interface for Level 11 Sandbox."""

from __future__ import annotations

import typer

from agentos.sandbox_orchestrator import SandboxOrchestrator

sandbox_app = typer.Typer(
    name="sandbox",
    help="Level 11 isolated sandbox commands (Stage A & Stage B fail-closed).",
    no_args_is_help=True,
)


@sandbox_app.command(name="preflight")
def preflight() -> None:
    """Run Stage A integrity and Stage B container runtime preflight."""
    orchestrator = SandboxOrchestrator()
    typer.echo("=== Sandbox Preflight Checks ===")

    # 1. Kill switch
    kill_ok, kill_msg = orchestrator.check_kill_switch()
    typer.echo(f"Kill Switch: [{'PASS' if kill_ok else 'FAIL'}] {kill_msg}")

    # 2. Stage A Integrity
    stage_a_ok, stage_a_msg = orchestrator.verify_stage_a_integrity()
    typer.echo(f"Stage A Integrity: [{'PASS' if stage_a_ok else 'FAIL'}] {stage_a_msg}")

    # 3. Runtime Preflight
    runtime_ok, runtime_msg, engine = orchestrator.check_runtime_preflight()
    typer.echo(f"Container Runtime: [{'PASS' if runtime_ok else 'BLOCKED'}] {runtime_msg}")

    if not (kill_ok and stage_a_ok and runtime_ok):
        typer.echo("\nPreflight result: BLOCKED (Fail-Closed). Execution disabled.")
        raise typer.Exit(code=1)

    typer.echo("\nPreflight result: READY.")


@sandbox_app.command(name="run")
def run(
    cmd: str = typer.Argument(..., help="Allowlisted test command to execute (e.g. 'pytest')"),
) -> None:
    """Execute an allowlisted test command inside the isolated Stage B container."""
    orchestrator = SandboxOrchestrator()
    result = orchestrator.execute(cmd)

    typer.echo(f"Run ID: {result.run_id}")
    typer.echo(f"Status: {result.status}")
    typer.echo(f"Exit Code: {result.exit_code}")
    if result.stdout:
        typer.echo(f"\nStdout:\n{result.stdout}")
    if result.stderr:
        typer.echo(f"\nStderr:\n{result.stderr}")
    if result.error_message:
        typer.echo(f"\nError: {result.error_message}")

    raise typer.Exit(code=result.exit_code)
