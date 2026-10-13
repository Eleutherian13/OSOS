-- Prompt 4 additive migration (idempotent; preserves V012 + all earlier)
-- Issue/Hunter evidence tables; no destructive changes; SQLite only
CREATE TABLE IF NOT EXISTS issue_record (
    id TEXT PRIMARY KEY,
    repo_org TEXT,
    repo_name TEXT,
    issue_number INTEGER,
    issue_url TEXT,
    title TEXT,
    status TEXT,
    assignee TEXT,
    retrieved_at TEXT,
    observation_timestamp TEXT,
    evidence_refs TEXT,
    transition_history TEXT,
    source_hash TEXT
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS idx_issue_repo ON issue_record(repo_org, repo_name);
CREATE INDEX IF NOT EXISTS idx_issue_status ON issue_record(status);
-- Evidence bundle extension (additive only; V003 schema preserved)
CREATE TABLE IF NOT EXISTS issue_evidence_bundle (
    issue_id TEXT,
    observed_at TEXT,
    kind TEXT,
    source_ref TEXT,
    note TEXT,
    raw_body_stored INTEGER DEFAULT 0,
    FOREIGN KEY (issue_id) REFERENCES issue_record(id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_ev_bundle_issue ON issue_evidence_bundle(issue_id, observed_at);
