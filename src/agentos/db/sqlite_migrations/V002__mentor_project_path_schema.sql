-- V002: Mentor Project Path (complete schema, SQLite).
create table if not exists organizations (
    id text primary key,
    name text not null,
    slug text not null unique,
    created_at datetime not null default (datetime('now'))
);

create table if not exists projects (
    id text primary key,
    org_id text not null references organizations(id),
    title text not null,
    slug text not null,
    repo_url text,
    description text,
    created_at datetime not null default (datetime('now')),
    unique (org_id, slug)
);

create table if not exists mentors (
    id text primary key,
    org_id text not null references organizations(id),
    handle text not null,
    contact_channel_hint text,
    created_at datetime not null default (datetime('now')),
    unique (org_id, handle)
);

create table if not exists paths (
    id text primary key,
    org_id text not null references organizations(id),
    project_id text not null references projects(id),
    mentor_id text references mentors(id),
    path_type text not null check (path_type in ('gsoc', 'lfx', 'other')),
    path_slug text not null,
    state text not null default 'WATCH' check (state in ('WATCH','ENGAGED','ACTIVE','BACKUP','DROPPED')),
    created_at datetime not null default (datetime('now')),
    updated_at datetime not null default (datetime('now')),
    unique (org_id, path_slug)
);

create table if not exists prerequisites (
    id text primary key,
    path_id text not null references paths(id) on delete cascade,
    description text not null,
    estimated_hours real not null check (estimated_hours > 0),
    order_index integer not null default 0,
    created_at datetime not null default (datetime('now'))
);

create table if not exists interactions (
    id text primary key,
    path_id text not null references paths(id) on delete cascade,
    interaction_type text not null check (interaction_type in ('email','issue','pr','meeting','other')),
    direction text not null check (direction in ('inbound','outbound','mutual')),
    level integer not null check (level >= 0 and level <= 7),
    link text not null,
    channel text not null default 'UNKNOWN' check (channel in ('PUBLIC','PRIVATE','UNKNOWN')),
    quote text,
    summary text,
    occurred_at datetime not null default (datetime('now')),
    created_at datetime not null default (datetime('now'))
);

create table if not exists followups (
    id text primary key,
    path_id text not null references paths(id) on delete cascade,
    interaction_id text references interactions(id) on delete set null,
    state text not null default 'pending' check (state in ('pending','completed','cancelled')),
    due_at datetime not null,
    note text,
    created_at datetime not null default (datetime('now')),
    unique (interaction_id)
);

create index if not exists idx_interaction_path on interactions(path_id, occurred_at desc);
create index if not exists idx_followup_path_state on followups(path_id, state, due_at);
