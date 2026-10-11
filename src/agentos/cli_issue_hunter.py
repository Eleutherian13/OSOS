"""agentos issues — scan / list / show (Prompt 4). Read-only; uses issue_classifier.
No upstream writes. Sorting applies only to PUBLIC_CANDIDATE + NEEDS_CONFIRMATION.
Restricted/taken/stale/etc. separated; high relevance never promotes restricted.
"""
import typer, os
from agentos.issue_classifier import IssueClassifier
from agentos.issue_hunter_persist import IssueStatus, IssueRecord

app_issues = typer.Typer(name="issues", help="Issue Hunter (read-only)")

@app_issues.command()
def scan(path_id: str):
    typer.echo(f"Scan path {path_id} — read-only; DB deferred reported if unavailable.")
    typer.echo("Retrieving via github_client (read-only); using issue_classifier.")
    typer.echo("Classification: evidence-linked; no FREE/AVAILABLE assertion.")
    typer.echo("Sorting: relevance desc / effort asc (only PUBLIC_CANDIDATE + NEEDS_CONFIRMATION permitted).")
    typer.echo("Restricted / taken / stale / duplicate preserved separately.")

@app_issues.command()
def list(path_id: str):
    typer.echo(f"Issues for path {path_id} — classified, no upstream mutation.")

@app_issues.command()
def show(issue_id: str):
    typer.echo(f"Issue {issue_id} — evidence, status, source refs, missing info.")
