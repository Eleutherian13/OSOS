"""Level 9 — Issue Hunter (read-only evidence fetcher; NOT a PR/issue writer).
Reads from GitHub (fixture/test-double when network unavailable); writes to evidence
ledger only via existing EvidenceRepo (read-side integration); never claims/posts/updates.
Requires github_client; does NOT implement Issue Hunter if client missing — documents.
"""
from __future__ import annotations
from agentos.github_client import GitHubClient

class IssueHunter:
    """Read-only discovery of candidate issues / PRs for ranking input.
    No claim posting. No maintainer notification. No upstream change."""

    def __init__(self, client: GitHubClient | None = None):
        self.client = client or GitHubClient()
        self.read_only = True
        self.upstream_write_attempted = False

    def hunt(self, org: str, repo: str) -> dict:
        # Real: fetch open/closed issues + PRs; filter by relevance / public-candidate / needs-confirmation
        # Here: DB/network deferred -> structured missing (not fabricated records)
        return {
            "org": org, "repo": repo,
            "issues_found": 0,
            "pr_found": 0,
            "classification": {},
            "status": "NOT_VERIFIED — DB/network deferred; fixtures only",
            "read_only": True,
            "fabricated_records": False,
            "public_candidate_promotion": False,
            "socially_restricted_preserved": True,
        }
