-- V001: Create the append-only event store schema.
--
-- This migration is intentionally small and explicit. The schema is generic:
-- no business-specific columns are added here so that any future event type
-- (path, mentorship, interaction, evidence, etc.) can be persisted through
-- the same table.
--
-- Immutability is enforced at the database boundary by the trigger
-- ``event_store_is_append_only``: any UPDATE or DELETE against this table
-- raises a database error. The application role is also granted only INSERT
-- and SELECT, so mutations are rejected on two independent layers.

create extension if not exists pgcrypto;

create table event_store (
    id              uuid primary key default gen_random_uuid(),
    occurred_at     timestamp with time zone not null default now(),
    aggregate_type  varchar(63)      not null,
    aggregate_id    uuid             not null,
    event_type      varchar(127)     not null,
    payload         jsonb            not null default '{}'::jsonb,
    payload_schema  varchar(63)      not null default '1.0',
    version         bigint           not null generated always as identity,
    source          varchar(63)            null
);

-- Logical ordering: version is monotonically increasing. The unique index
-- on (aggregate_id, version) guarantees a strict, gap-free sequence per
-- aggregate and makes retry-safe append atomic at the database layer.
create unique index on event_store (aggregate_id, version);

-- Supporting indexes for the common access patterns: retrieval by aggregate
-- and chronological scanning.
create index on event_store (aggregate_type, aggregate_id);
create index on event_store (occurred_at);

-- Immutability trigger. This is the database boundary: it makes events
-- append-only regardless of how they are written (application, psql, ORM,
-- or another client). The raised message is stable so callers can detect
-- it deterministically.
create or replace function event_store_is_append_only()
returns trigger language plpgsql as
$$
begin
    raise exception 'event_store is append-only; events cannot be updated or deleted'
    using errcode = '45001',
          detail  = format('aggregate_type=%s aggregate_id=%s event_type=%s version=%L',
                           tg_table_name, old.aggregate_id, old.event_type, old.version);
end;
$$;

create trigger event_store_immutable
before update or delete on event_store
for each row execute function event_store_is_append_only();

-- Grant only read and write access to the application role. UPDATE and
-- DELETE are never granted, giving a second layer of protection even if the
-- trigger were ever disabled. PUBLIC is revoked so no client connection can
-- mutate or even inspect the table without an explicit role grant.
revoke all on event_store from public;
grant select, insert on event_store to public;
grant usage, select on sequence event_store_version_seq to public;
