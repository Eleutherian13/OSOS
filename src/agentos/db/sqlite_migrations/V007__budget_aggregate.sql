-- V007: Budget aggregates — rolling 30-day (SQLite).

create table if not exists budget (
    id text primary key,
    period_start date not null,
    agent text not null,
    cap real not null check (cap >= 0),
    spent real not null default 0 check (spent >= 0),
    updated_at datetime not null default (datetime('now')),
    unique (period_start, agent)
);

