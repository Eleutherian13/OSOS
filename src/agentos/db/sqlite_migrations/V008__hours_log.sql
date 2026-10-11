-- V008: Persistent hours log (SQLite).

create table if not exists hours_log (
    id text primary key,
    agent text not null,
    category text not null check (category in ('tool','evidence')),
    hours real not null check (hours > 0),
    recorded_at datetime not null default (datetime('now')),
    evidence_ref text references evidence(id) on delete set null
);

create index if not exists idx_hours_log_agent_category on hours_log(agent, category);

