-- V003: Evidence ledger (Level 3), interaction channel, readiness fact
create extension if not exists pgcrypto;

-- Evidence ledger (additive; references existing paths)
create table if not exists evidence (
    id uuid primary key default gen_random_uuid(),
    path_id uuid not null references paths(id) on delete cascade,
    claim text not null,
    artifact_url text not null,
    kind varchar(31) not null check (kind in ('fix','test_infra','design','review','community')),
    depth smallint not null check (depth between 1 and 5),
    relevance_to_project numeric(4,3) not null check (relevance_to_project between 0 and 1),
    project_specificity numeric(4,3) not null check (project_specificity between 0 and 1),
    independence smallint not null check (independence between 1 and 5),
    maintainer_signal numeric(3,1) not null check (maintainer_signal between -1 and 1),
    mentor_validated boolean not null default false,
    understood boolean not null default false,
    interaction_id uuid references interactions(id) on delete set null,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now()
);

create index if not exists idx_evidence_path_kind on evidence(path_id, kind);
create index if not exists idx_evidence_path_validated on evidence(path_id, mentor_validated);
create index if not exists idx_evidence_path_specificity on evidence(path_id, project_specificity);

-- Interaction public-channel flag (smallest additive; default UNKNOWN never satisfies R2)
alter table interactions add column if not exists channel varchar(15) not null default 'UNKNOWN' check (channel in ('PUBLIC','PRIVATE','UNKNOWN'));

-- Readiness fact table (per Prompt 0 provenance strategy; separate audit from artifacts)
create table if not exists readiness_fact (
    id uuid primary key default gen_random_uuid(),
    path_id uuid not null references paths(id) on delete cascade,
    fact_type varchar(63) not null check (fact_type in ('R1','R2','R3','R4_tests','R4_template','R4_review','R5_direction','R5_assessment')),
    satisfied boolean not null default false,
    evidence_ref uuid references evidence(id) on delete set null,
    interaction_ref uuid references interactions(id) on delete set null,
    recorded_at timestamp with time zone not null default now()
);

create index if not exists idx_readiness_path_fact on readiness_fact(path_id, fact_type);
