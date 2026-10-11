-- V003: Evidence ledger + interaction channel + readiness fact (SQLite).

create table if not exists evidence (
    id text primary key,
    path_id text not null references paths(id) on delete cascade,
    claim text not null,
    artifact_url text not null,
    kind text not null check (kind in ('fix','test_infra','design','review','community')),
    depth integer not null check (depth between 1 and 5),
    relevance_to_project real not null check (relevance_to_project between 0 and 1),
    project_specificity real not null check (project_specificity between 0 and 1),
    independence integer not null check (independence between 1 and 5),
    maintainer_signal real not null check (maintainer_signal between -1 and 1),
    mentor_validated boolean not null default 0,
    understood boolean not null default 0,
    interaction_id text references interactions(id) on delete set null,
    created_at datetime not null,
    updated_at datetime not null
);

create index if not exists idx_evidence_path_kind on evidence(path_id, kind);
create index if not exists idx_evidence_path_validated on evidence(path_id, mentor_validated);
create index if not exists idx_evidence_path_specificity on evidence(path_id, project_specificity);

create table if not exists readiness_facts (
    id text primary key,
    path_id text not null references paths(id) on delete cascade,
    fact_type text not null,
    fact_value text not null,
    source_ref text,
    verified_at datetime,
    created_at datetime not null,
    unique (path_id, fact_type)
);

