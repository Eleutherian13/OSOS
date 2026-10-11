-- Level 9 Prompt 2 — Issue Hunter additive migration (idempotent, compatible with V003)
create table if not exists issue_hunter_issues (
    id uuid primary key default gen_random_uuid(),
    repo_org text not null,
    repo_name text not null,
    issue_url text not null,
    issue_number int not null,
    title text not null,
    status text not null check (status in ('PUBLIC_CANDIDATE','NEEDS_CONFIRMATION','CONFIRMED','IN_PROGRESS','DONE','LIKELY_TAKEN','DUPLICATE','STALE','OUT_OF_SCOPE','SOCIALLY_RESTRICTED')),
    labels text[],
    assignee text,
    author_role text not null default 'unknown' check (author_role in ('maintainer','contributor','unknown')),
    source_hash text,
    retrieved_at timestamp with time zone,
    observation_timestamp timestamp with time zone,
    transition_history jsonb default '[]',
    evidence_refs text[],
    note text,
    raw_body_stored boolean not null default false,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    unique (repo_org, repo_name, issue_number)
);
create index if not exists idx_issue_status_obs on issue_hunter_issues(status, observation_timestamp desc);
