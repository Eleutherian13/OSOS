-- V004: Registry projection (SQLite).

create table if not exists org_policy (
    id text primary key,
    org_slug text not null unique,
    policy_surface text not null,
    policy_value text not null check (policy_value in ('BLOCKED','ASSIST_ONLY','DISCLOSE','ALLOWED','UNKNOWN')),
    source_ref text not null,
    registry_digest text not null,
    updated_at datetime not null
);

create table if not exists org_mode (
    id text primary key,
    org_slug text not null unique,
    effective_mode text not null check (effective_mode in ('OBSERVE','UNDERSTANDING_ONLY','ASSIST','COPILOT')),
    code_policy text not null,
    autonomous_policy text not null,
    derived_from_digest text not null,
    human_confirmed boolean not null default 0,
    reconfirmation_needed boolean not null default 0,
    updated_at datetime not null
);

create table if not exists contact_rules (
    id text primary key,
    org_slug text not null unique,
    rules_json text not null,
    source_ref text,
    updated_at datetime not null
);

