-- V002: MentorProjectPath domain tables + prerequisites + interactions + followups
create extension if not exists pgcrypto;

create table if not exists organizations (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    slug text not null unique,
    created_at timestamp with time zone not null default now()
);

create table if not exists projects (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references organizations(id) on delete restrict,
    title text not null,
    slug text not null,
    repo_url text,
    description text,
    created_at timestamp with time zone not null default now(),
    unique (org_id, slug)
);

create table if not exists mentors (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references organizations(id) on delete restrict,
    handle text not null,
    contact_channel_hint text,
    created_at timestamp with time zone not null default now(),
    unique (org_id, handle)
);

create table if not exists paths (
    id uuid primary key default gen_random_uuid(),
    org_id uuid not null references organizations(id) on delete restrict,
    project_id uuid not null references projects(id) on delete restrict,
    state text not null default 'WATCH'
        check (state in ('WATCH','ENGAGED','ACTIVE','BACKUP','DROPPED')),
    created_at timestamp with time zone not null default now()
);

create table if not exists prerequisites (
    id uuid primary key default gen_random_uuid(),
    path_id uuid not null references paths(id) on delete cascade,
    title text not null,
    resolved boolean not null default false,
    note text,
    seq smallint not null default 0,
    created_at timestamp with time zone not null default now()
);

create table if not exists interactions (
    id uuid primary key default gen_random_uuid(),
    path_id uuid not null references paths(id) on delete cascade,
    direction text not null check (direction in ('inbound','outbound')),
    level smallint not null check (level >= 0 and level <= 7),
    link text not null,
    occurred_at timestamp with time zone not null default now(),
    quote text,
    note text,
    created_at timestamp with time zone not null default now(),
    unique (path_id, link)
);

create table if not exists followups (
    id uuid primary key default gen_random_uuid(),
    path_id uuid not null references paths(id) on delete cascade,
    interaction_id uuid references interactions(id) on delete set null,
    state text not null default 'pending' check (state in ('pending','completed','cancelled')),
    due_at timestamp with time zone not null,
    created_at timestamp with time zone not null default now(),
    unique (interaction_id)
);

create index idx_interaction_path on interactions(path_id, occurred_at desc);
create index idx_followup_path_state on followups(path_id, state, due_at);
