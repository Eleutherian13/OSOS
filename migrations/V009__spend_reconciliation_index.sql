-- V009: Spend detail event reconciliation (reuses append-only event_store; no redundant ledger)
-- Spend events reference budget aggregate; budget update is transactional companion.
-- Existing event_store (V001) already append-only (trigger + role). No new mutation table needed.
-- If additional reconciliation index required, add here; otherwise rely on event_store payload.

-- Optional: index on event_store for financial reconciliation (non-mutating, idempotent)
create index if not exists idx_event_store_spend_reconcile
    on event_store (aggregate_type, occurred_at)
    where aggregate_type = 'spend';
