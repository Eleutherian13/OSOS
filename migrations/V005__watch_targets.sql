-- V005: Watch targets (Level 5 Prompt 1), additive, idempotent
create extension if not exists pgcrypto;

create table if not exists watch_targets (
    id uuid primary key default gen_random_uuid(),
    target_id varchar(63) not null unique,
    url text not null,
    category varchar(31) not null check (category in (
        'GSoC_TIMELINE','GSoC_RULES','GSoC_AI_GUIDANCE',
        'LFX_DOCS','ORG_CONTRIBUTING','ORG_AI_POLICY',
        'ORG_PROJECT_IDEAS','ORG_CONTACT')),
    enabled boolean not null default true,
    org_slug varchar(63),
    program_name varchar(127),
    source_ref varchar(63),
    observed_sha256 char(64),
    etag varchar(63),
    last_modified varchar(63),
    last_success_check timestamp with time zone,
    operational_status varchar(31) not null default 'PENDING' check (operational_status in ('OK','STALE','ERROR','PENDING')),
    last_error_summary text,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now()
);

create index if not exists idx_watch_targets_target_id on watch_targets(target_id);
create index if not exists idx_watch_targets_category on watch_targets(category);
create index if not exists idx_watch_targets_org_slug on watch_targets(org_slug);
create index if not exists idx_watch_targets_enabled on watch_targets(enabled) where enabled;
