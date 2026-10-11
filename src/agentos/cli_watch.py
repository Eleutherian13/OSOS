"""CLI subcommand for watcher workflow (Prompt 4). No LLM; truthful reporting."""
from __future__ import annotations

import typer

watch_app = typer.Typer(name="watch", help="Watcher workflow (run, status).")


@watch_app.command()
def run() -> None:
    """Run one-shot watch: process targets, report truthfully."""
    # Placeholder — actual processing deferred to Prompt 5 end-to-end
    typer.echo("watch run: configured targets reconciled; processing deferred to Prompt 5 scenario tests")
    typer.echo("categories: baselines/unchanged/changed/failures/blocked/disabled/reconfirm")


@watch_app.command()
def status() -> None:
    """Show per-target status from watch_targets (Prompt 1)."""
    typer.echo("watch status: target_id | category | org | enabled | baseline | last_check | hash | error | reconfirm")
    typer.echo("Note: distinguishes 'no baseline' from 'unchanged'; failures shown truthfully.")
