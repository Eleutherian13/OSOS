-- V005: Watch targets (SQLite).

create table if not exists watch_targets (
    id text primary key,
    target_id text not null unique,
    url text not null,
    category text not null check (category in (
        'GSoC_TIMELINE','GSoC_RULES','GSoC_AI_GUIDANCE',
        'LFX_DOCS','ORG_CONTRIBUTING','ORG_AI_POLICY',
        'ORG_PROJECT_IDEAS','ORG_CONTACT')),
    enabled boolean not null default 1,
    org_slug text,
    program_name text,
    source_ref text,
    observed_sha256 text,
    etag text,
    last_modified text,
    last_success_check datetime,
    operational_status text not null default 'PENDING' check (operational_status in ('OK','STALE','ERROR','PENDING')),
    last_error_summary text,
    created_at datetime not null,
    updated_at datetime not null
);

create index if not exists idx_watch_targets_target_id on watch_targets(target_id);
create index if not exists idx_watch_targets_category on watch_targets(category);
create index if not exists idx_watch_targets_org_slug on watch_targets(org_slug);
create index if not exists idx_watch_targets_enabled on watch_targets(enabled);

