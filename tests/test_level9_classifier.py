"""Prompt 3 tests — deterministic classifier; exact language; no FREE/AVAILABLE; restrictions preserved."""
from agentos.issue_classifier import IssueClassifier, Signal
from agentos.issue_hunter_persist import IssueStatus, IssueRecord

def test_no_free_available_language():
    c = IssueClassifier()
    r = IssueRecord(id="i1", repo_org="o", repo_name="r", issue_url="http://x/1", issue_number=1, title="t", status=IssueStatus.PUBLIC_CANDIDATE, author_role="unknown")
    res = c.classify(r, [])
    assert res["proposed_state"] == IssueStatus.PUBLIC_CANDIDATE.value
    assert "FREE" not in res["reason"]
    assert "AVAILABLE" not in res["reason"]
    assert "No public evidence that someone else is on this" in res["reason"]

def test_maintainer_reply_required_for_confirmed():
    c = IssueClassifier()
    r = IssueRecord(id="i2", repo_org="o", repo_name="r", issue_url="http://x/2", issue_number=2, title="t", status=IssueStatus.PUBLIC_CANDIDATE)
    res = c.classify(r, [Signal("strong","e1","2026-10-01","maintainer reply logged",0.9)])
    assert res["proposed_state"] == IssueStatus.CONFIRMED.value

def test_explicit_claim_likely_taken():
    c = IssueClassifier()
    r = IssueRecord(id="i3", repo_org="o", repo_name="r", issue_url="http://x/3", issue_number=3, title="t", status=IssueStatus.PUBLIC_CANDIDATE)
    res = c.classify(r, [Signal("medium","e1","2026-10-02","I'll take this",0.7)])
    assert res["proposed_state"] == IssueStatus.LIKELY_TAKEN.value

def test_restriction_prevents_eligible():
    c = IssueClassifier()
    r = IssueRecord(id="i4", repo_org="o", repo_name="r", issue_url="http://x/4", issue_number=4, title="t", status=IssueStatus.PUBLIC_CANDIDATE)
    res = c.classify(r, [Signal("restricted","e1","2026-10-01","needs-design / core team",0.8)])
    assert res["proposed_state"] == IssueStatus.SOCIALLY_RESTRICTED.value

def test_weak_signal_not_decisive():
    c = IssueClassifier()
    r = IssueRecord(id="i5", repo_org="o", repo_name="r", issue_url="http://x/5", issue_number=5, title="t", status=IssueStatus.PUBLIC_CANDIDATE)
    res = c.classify(r, [Signal("weak","e1","2026-10-01","branch name contains issue#",0.2)])
    assert res["proposed_state"] == IssueStatus.NEEDS_CONFIRMATION  # weak alone → conservative unresolved

def test_conflicting_evidence_conservative():
    c = IssueClassifier()
    r = IssueRecord(id="i6", repo_org="o", repo_name="r", issue_url="http://x/6", issue_number=6, title="t", status=IssueStatus.PUBLIC_CANDIDATE)
    # Strong claim + restriction
    res = c.classify(r, [Signal("strong","e1","2026-10-01","working",0.9), Signal("restricted","e2","2026-10-02","needs-design",0.8)])
    assert res["proposed_state"] == IssueStatus.SOCIALLY_RESTRICTED.value  # restriction overrides

def test_no_model_override():
    res = IssueClassifier().classify(IssueRecord(id="i",repo_org="o",repo_name="r",issue_url="http://x/i",issue_number=1,title="t",status=IssueStatus.PUBLIC_CANDIDATE,author_role="unknown"), [])
    assert res["no_model_override"] is True
    assert res["no_free_assertion"] is True
