-- V001: Create the append-only event store schema (SQLite).
-- UUIDs stored as text, timestamps as ISO strings.
-- Immutability enforced at application layer (trigger replaced by app validation).

create table if not exists event_store (
    id              text primary key,
    occurred_at     text not null,
    aggregate_type  text not null,
    aggregate_id    text not null,
    event_type      text not null,
    payload         text not null default '{}',
    payload_schema  text not null default '1.0',
    version         integer not null default 1,
    source          text
);

create unique index if not exists idx_event_store_aggregate_version
    on event_store (aggregate_id, version);

create index if not exists idx_event_store_aggregate_type
    on event_store (aggregate_type, aggregate_id);

create index if not exists idx_event_store_occurred_at
    on event_store (occurred_at);

