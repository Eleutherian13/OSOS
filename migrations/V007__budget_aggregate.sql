-- V007: Budget aggregates (rolling 30-day, additive, idempotent)
-- Period definition: rolling 30-day window; enforced in service layer (not month column).
-- Uniqueness: (period_start, agent) prevents duplicate aggregates per retry.

create table if not exists budget (
    id uuid primary key default gen_random_uuid(),
    period_start date not null,
    agent varchar(63) not null,
    cap numeric(10,2) not null check (cap >= 0),
    spent numeric(10,2) not null default 0 check (spent >= 0),
    updated_at timestamp with time zone not null default now(),
    unique (period_start, agent)
);

-- Constraints reject invalid monetary amounts (check above) and duplicate period/agent.
-- No reset of historical data; table is additive only.
