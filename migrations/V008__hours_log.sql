-- V008: Persistent hours log (tool-hours + evidence-hours per CLI spec)
-- Rejects zero / negative / nonnumeric quantities via application layer + DB check.

create table if not exists hours_log (
    id uuid primary key default gen_random_uuid(),
    agent varchar(63) not null,
    category varchar(31) not null check (category in ('tool','evidence')),
    hours numeric(6,2) not null check (hours > 0),
    recorded_at timestamp with time zone not null default now(),
    evidence_ref uuid null references evidence(id) on delete set null
);

create index if not exists idx_hours_log_agent_category on hours_log(agent, category);
