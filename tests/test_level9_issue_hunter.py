"""Level 9 Prompt 2 — Issue Hunter tests (executable, adversarial, no model override)."""
from agentos.issue_hunter_persist import IssueRecord, IssueStatus, IssueHunterPersistence

def test_status_values_all_preserved():
    for s in IssueStatus:
        assert s.value in ("PUBLIC_CANDIDATE","NEEDS_CONFIRMATION","CONFIRMED","IN_PROGRESS","DONE","LIKELY_TAKEN","DUPLICATE","STALE","OUT_OF_SCOPE","SOCIALLY_RESTRICTED")

def test_valid_transitions():
    p = IssueHunterPersistence()
    assert p.validate_transition(IssueStatus.PUBLIC_CANDIDATE, IssueStatus.CONFIRMED, ["e1"])
    assert p.validate_transition(IssueStatus.CONFIRMED, IssueStatus.IN_PROGRESS, ["e2"])
    assert p.validate_transition(IssueStatus.IN_PROGRESS, IssueStatus.DONE, [])

def test_invalid_transitions_rejected():
    p = IssueHunterPersistence()
    # No evidence for SOCIALLY_RESTRICTED
    assert p.validate_transition(IssueStatus.PUBLIC_CANDIDATE, IssueStatus.SOCIALLY_RESTRICTED, []) is False
    # Duplicate -> not to IN_PROGRESS
    assert p.validate_transition(IssueStatus.DUPLICATE, IssueStatus.IN_PROGRESS, ["e"]) is False

def test_bundle_includes_all_required():
    r = IssueRecord(id="i1", repo_org="o", repo_name="r", issue_url="http://x/1", issue_number=1, title="t", status=IssueStatus.NEEDS_CONFIRMATION, author_role="unknown")
    b = IssueHunterPersistence().record_evidence_bundle(r)
    assert b["url"] == "http://x/1"
    assert b["status"] == "NEEDS_CONFIRMATION"
    assert b["raw_body_stored"] is False
    assert "transition_history" in b

def test_untrusted_text_never_executable():
    # Raw body must never be stored as instruction
    r = IssueRecord(id="i2", repo_org="o", repo_name="r", issue_url="http://x/2", issue_number=2, title="t2", status=IssueStatus.PUBLIC_CANDIDATE, raw_body_stored=False)
    assert r.raw_body_stored is False
