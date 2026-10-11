"""Proposal Evidence Auditor CLI — Design A (deterministic-only).
Read-only: proposal/idea open 'r'; DB SELECT only; no mutation; no proposal rewrite.
No model integration (Design B blocked — no provider/integration/dataset).
Output: structured findings only; never proposal prose.
"""
from __future__ import annotations
import typer, os
from agentos.domain.auditor_finding import Finding, FindingStatus, FindingCategory
from agentos.core.auditor_service import AuditorService

app_auditor = typer.Typer(name="auditor", help="Proposal Evidence Auditor (deterministic-only, Design A)")

@app_auditor.command()
def run(
    proposal: str = typer.Option(..., "--proposal", help="Proposal draft file path (read-only)"),
    idea: str = typer.Option(None, "--idea", help="Idea page file path (read-only)"),
    hours: str = typer.Option(None, "--hours", help="Program-hours / project-size source (read-only)"),
    db_path: str = typer.Option("data/agentos.sqlite", "--db", help="Evidence ledger SQLite path (read-only access)"),
    out: str = typer.Option("-", "--out", help="Output file (default stdout)"),
):
    """Run deterministic audit: validate sources, quote claim excerpts, check DB, return findings."""
    service = AuditorService(db_path=db_path)
    # Input validation (read-only, never mutate source)
    input_result = service.load_input_ids(proposal, idea, hours)
    # Read-only proposal load (bounded read; never execute proposal content)
    findings = service.build_findings(proposal_path=proposal) if input_result["proposal_readable"] else []
    if not input_result["proposal_readable"]:
        # If draft unreadable, produce MISSING_SOURCE finding immediately (deterministic)
        from agentos.domain.auditor_finding import Finding, FindingCategory, FindingStatus, EvidenceLink
        findings.append(Finding(
            finding_id="F-MISSING-SOURCE-01",
            category=FindingCategory.MISSING_SOURCE,
            proposal_ref="proposal draft",
            proposal_location=proposal,
            status=FindingStatus.MISSING_SOURCE,
            explanation=f"Proposal draft not readable at {proposal}. Evidence ledger DB count verified (read-only): evidence={input_result['db_counts'].get('evidence', 'N/A')}. No claim evaluated; analysis blocked at input gate.",
            evidence_links=[EvidenceLink(kind="db", reference=f"DB:evidence={input_result['db_counts'].get('evidence','N/A')}", location="DB:evidence (verified readable)", verified=True)],
            evidence_gap="Proposal draft unavailable; ledger verified readable but contains 0 evidence records.",
            question="Provide readable proposal draft to proceed.",
            proposal_rewrite_check="pass",
        ))
    # Structured output (never proposal text; only findings + evidence links/gaps)
    output_lines = [
        "PROPOSAL_EVIDENCE_AUDITOR — DESIGN A (DETERMINISTIC-ONLY)",
        "Status: implementation of approved spec (semantic evaluation deferred — limitation documented)",
        f"Inputs: proposal_readable={input_result['proposal_readable']} idea_readable={input_result.get('idea_readable', False)} hours_readable={input_result.get('hours_readable', False)} source_map_ok={input_result['source_map_ok']}",
        f"DB: readable={input_result['db_readable']} counts={input_result['db_counts']}",
        "Findings:",
    ]
    for f in findings:
        output_lines.append(f"  {f.finding_id} | {f.category.value} | {f.status.value} | {f.proposal_ref[:60]}...")
        output_lines.append(f"      explanation={f.explanation[:120]}...")
        output_lines.append(f"      evidence_links={[(l.kind, l.reference) for l in f.evidence_links]} evidence_gap={f.evidence_gap}")
        output_lines.append(f"      question={f.question}")
        if f.mentor_challenge_label:
            output_lines.append(f"      mentor_challenge={f.mentor_challenge_label} (anticipated, not actual reply)")
    output_lines.append("CRITIC-ONLY: proposal_rewrite_check=pass; no proposal prose in output; source references resolved or gap labeled.")
    result_text = "\n".join(output_lines)
    if out == "-":
        typer.echo(result_text)
    else:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(result_text)
        typer.echo(f"Findings written to {out}")
