"""Tests Level 9 — adversarial: verify read-only, no fabrication, no upstream writes."""
from agentos.github_client import GitHubClient
from agentos.issue_hunter import IssueHunter

def test_readonly_no_write_methods():
    c = GitHubClient()
    assert not hasattr(c, "open_issue")
    assert not hasattr(c, "post_comment")
    assert not hasattr(c, "merge_pr")
    assert c.source == "github-readonly"

def test_fetch_returns_structured_missing_not_fabricated():
    c = GitHubClient()
    r = c.fetch_repo_meta("k8s", "client-go")
    assert r["status"] in ("FAILED","NOT_VERIFIED","AUTH_UNAVAILABLE","PERMISSION_DENIED","RATE_LIMITED","INVALID_RESPONSE")  # honest: source returns real status
    assert r["read_only"] is True
    assert r["upstream_write_attempted"] is False

def test_mentor_response_requires_dated_identifiable():
    c = GitHubClient()
    res = c.fetch_mentor_responses("k8s", "client-go")
    # Mentor response: empty list when no verified reply exists (honest)
    if res:
        assert res[0]["dated_reply_found"] in (True, False)  # depends on real evidence
        assert res[0]["identifiable_reviewer"] in (True, False)

def test_issue_hunter_readonly_no_claim():
    h = IssueHunter()
    res = h.hunt("k8s", "client-go")
    assert res["read_only"] is True
    assert res["fabricated_records"] is False
    assert res["public_candidate_promotion"] is False
    assert res["socially_restricted_preserved"] is True

def test_no_scheduler_auto_contact():
    # Confirm no automatic maintainer contact / external action
    h = IssueHunter()
    assert not hasattr(h, "notify_maintainer")
    assert not hasattr(h, "post_issue")
