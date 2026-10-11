-- V009: Spend reconciliation index (SQLite).
-- Reuses event_store; no new table needed.
-- Add index for financial reconciliation.

create index if not exists idx_event_store_spend_reconcile
    on event_store (aggregate_type, occurred_at);

