-- V006: Kill-state + outbox + approval token (SQLite).

create table if not exists kill_state (
    org_slug text primary key,
    epoch integer not null default 1,
    updated_at datetime not null default (datetime('now')),
    source text default 'db'
);

create table if not exists outbox_drafts (
    id text primary key,
    org_slug text not null,
    target_url text not null,
    body_sha256 text not null,
    state text not null default 'DRAFT' check (state in ('DRAFT','PENDING_APPROVAL','APPROVED','STALE','REJECTED','HANDED_OFF')),
    created_at datetime not null default (datetime('now')),
    updated_at datetime not null default (datetime('now')),
    approved_at datetime,
    expiry_at datetime,
    binding_sha256 text,
    target_etag text,
    approval_token text,
    kill_epoch integer
);

create table if not exists approval_tokens (
    id text primary key,
    outbox_id text not null references outbox_drafts(id) on delete cascade,
    token text not null unique,
    target_state_sha256 text not null,
    policy_hash text not null,
    kill_epoch integer not null,
    body_sha256 text not null,
    expires_at datetime not null,
    used_at datetime,
    created_at datetime not null default (datetime('now'))
);

insert or ignore into kill_state (org_slug, epoch, updated_at, source)
    values ('default', 1, datetime('now'), 'db');

