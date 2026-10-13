-- create table
CREATE TABLE IF NOT EXISTS path_mentors (
    id TEXT PRIMARY KEY,
    path_id TEXT NOT NULL REFERENCES paths(id) ON DELETE CASCADE,
    mentor_id TEXT NOT NULL REFERENCES mentors(id) ON DELETE CASCADE,
    joined_at DATETIME NOT NULL DEFAULT (datetime('now')),
    UNIQUE (path_id, mentor_id)
);
CREATE INDEX IF NOT EXISTS idx_path_mentors_path ON path_mentors(path_id);
CREATE INDEX IF NOT EXISTS idx_path_mentors_mentor ON path_mentors(mentor_id);
