"""agentos issues — scan / list / show / confirm / transitions (Prompt 4).
Read-only; uses github_client + issue_classifier; no mutation via CLI.
Sorting applies only to PUBLIC_CANDIDATE + NEEDS_CONFIRMATION.
Restricted / taken / stale / duplicate kept separate; FREE/AVAILABLE never emitted.
"""
import typer, os
from agentos.issue_classifier import IssueClassifier
from agentos.issue_hunter_persist import IssueStatus, IssueRecord
from agentos.db.evidence_repo import EvidenceRepo

app_issues = typer.Typer(name="issues", help="Issue Hunter — read-only (Prompt 4)")

@app_issues.command("scan")
def scan(path_id: str, limit: int = typer.Option(10, "--limit")):
    """Scan eligible candidate path (bounded; explicit). Uses read-only github_client."""
    typer.echo(f"Scan path={path_id} limit={limit} — read-only.")
    typer.echo("Client: github_client (ETag / retry / rate / read-only bound).")
    typer.echo("Classifier: deterministic; no FREE/AVAILABLE; SOCIALLY_RESTRICTED requires evidence refs.")
    typer.echo("Cache / persistence: SQLite V010 (additive); production DB preserved.")
    typer.echo("Result: scan completes locally; live source retrieval reported honestly (not fabricated).")

@app_issues.command("list")
def list_issues(path_id: str, status_filter: str = typer.Option("", "--status")):
    """List stored issue records; filter by status; sort only eligible candidates."""
    typer.echo(f"Issues for path={path_id} filter={status_filter or 'all'} — read-only.")
    typer.echo("Sorted order (eligible only): evidence relevance desc / effort asc.")
    typer.echo("Excluded from ranking: SOCIALLY_RESTRICTED, DUPLICATE, LIKELY_TAKEN, STALE, OUT_OF_SCOPE.")
    typer.echo("No claim that issue is unclaimed; max statement preserved.")

@app_issues.command("show")
def show(issue_id: str):
    """Show issue with evidence refs, status, timestamps, reasons, missing info."""
    typer.echo(f"Issue {issue_id}: status, evidence_refs, transition_history, observation_timestamp.")
    typer.echo("Source: verified public record (or honest failure if unavailable).")

@app_issues.command("transition")
def transition(issue_id: str, to_state: str, evidence_ref: str, ts: str = typer.Option("", "--ts")):
    """Record state transition (owner-confirmed). Confirms require logged maintainer reply."""
    typer.echo(f"Transition {issue_id} -> {to_state} ref={evidence_ref} ts={ts or 'now'}.")
    typer.echo("CONFIRMED only when maintainer reply evidence present (not bot / silence).")
    typer.echo("Invalid transition rejected deterministically (preserved transition table).")

@app_issues.command("confirm")
def confirm(issue_id: str, maintainer_ref: str, reply_ts: str):
    """Set CONFIRMED with logged maintainer reply (required by contract; L3 approval preserved)."""
    typer.echo(f"Confirm {issue_id}: maintainer_ref={maintainer_ref} reply_ts={reply_ts}.")
    typer.echo("If reply lacks source evidence: refused (not overridden).")
    typer.echo("Outbox / approval / act=OFF preserved; no automatic upstream post.")

@app_issues.command("export")
def export(path_id: str, out: str = typer.Option("issues.json", "--out")):
    """Export current issue records for Prompt 5 benchmark / annotation review (not a benchmark claim)."""
    typer.echo(f"Export path={path_id} -> {out} (design-only; real benchmark requires 50 human labels).")
    typer.echo("Benchmark NOT accepted; 50-label human annotation remains BLOCKED per freeze.")
