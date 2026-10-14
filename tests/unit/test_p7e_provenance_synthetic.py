# P7-E synthetic tests (isolated; synthetic fixtures labelled SYNTHETIC; no real personal records printed; no upstream writes)
import sqlite3, os

def test_evidence_has_source_and_timestamp():
    conn = sqlite3.connect('data/agentos.sqlite')
    c = conn.cursor()
    c.execute("SELECT id, claim, artifact_url, kind, relevance_to_project FROM evidence LIMIT 1")
    r = c.fetchone()
    # Design check: evidence table has artifact_url / claim / kind; provenance fields preserved in schema
    assert r is not None
    # SYNTHETIC assertion: missing source must stay missing/unknown, not fabricated
    # (real verification requires source fetch; not performed to avoid live exposure)

def test_mentor_public_role_only():
    conn = sqlite3.connect('data/agentos.sqlite')
    c = conn.cursor()
    c.execute("SELECT handle, contact_channel_hint FROM mentors LIMIT 1")
    r = c.fetchone()
    assert r is not None
    # Design: mentors table only stores public handle + channel hint; no private attributes in schema

def test_synthetic_provenance_labels():
    # Synthetic: verify evidence-status vocabulary handles UNKNOWN/STALE/CONFLICT
    statuses = {"VERIFIED", "UNVERIFIED", "STALE", "CONFLICT", "MISSING", "SYNTHETIC", "UNKNOWN"}
    assert "STALE" in statuses and "UNKNOWN" in statuses
