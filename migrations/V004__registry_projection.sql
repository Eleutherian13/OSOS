-- V004: Registry projection (Level 4), additive only, idempotent
create extension if not exists pgcrypto;

-- Canonical YAML is human-edited; PostgreSQL is queryable projection.
-- Each row references the registry digest to allow stale-projection detection.
create table if not exists org_policy (
    id uuid primary key default gen_random_uuid(),
    org_slug varchar(63) not null unique,
    policy_surface varchar(31) not null,
    policy_value varchar(31) not null check (policy_value in ('BLOCKED','ASSIST_ONLY','DISCLOSE','ALLOWED','UNKNOWN')),
    source_ref varchar(63) not null,
    registry_digest varchar(64) not null,
    updated_at timestamp with time zone not null default now()
);
create index if not exists idx_org_policy_slug on org_policy(org_slug);

create table if not exists org_mode (
    id uuid primary key default gen_random_uuid(),
    org_slug varchar(63) not null unique,
    effective_mode varchar(31) not null check (effective_mode in ('OBSERVE','UNDERSTANDING_ONLY','ASSIST','COPILOT')),
    code_policy varchar(31) not null,
    autonomous_policy varchar(31) not null,
    derived_from_digest varchar(64) not null,
    human_confirmed boolean not null default false,
    reconfirmation_needed boolean not null default false,
    updated_at timestamp with time zone not null default now()
);
create index if not exists idx_org_mode_slug on org_mode(org_slug);

create table if not exists contact_rules (
    id uuid primary key default gen_random_uuid(),
    org_slug varchar(63) not null unique,
    channel varchar(63) not null,
    direct_messages_welcome boolean not null default false,
    quote text not null,
    source_ref varchar(63) not null,
    registry_digest varchar(64) not null,
    updated_at timestamp with time zone not null default now()
);
create index if not exists idx_contact_rules_slug on contact_rules(org_slug);
