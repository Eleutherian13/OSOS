-- V006: Kill-state + outbox + approval token (additive; Prompt 3 / 4)
-- Conservative: one row per org; epoch monotonically increasing; STOP-file reconciliation.

CREATE TABLE IF NOT EXISTS kill_state (
    org_slug VARCHAR(63) PRIMARY KEY,
    epoch BIGINT NOT NULL DEFAULT 1,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    source VARCHAR(63) DEFAULT 'db'  -- db | stop_file
);

CREATE INDEX IF NOT EXISTS idx_kill_state_epoch ON kill_state(org_slug, epoch);

-- Initialize safely: insert only if missing (never reset existing)
INSERT INTO kill_state (org_slug, epoch, updated_at, source)
SELECT 'default', 1, now(), 'db'
WHERE NOT EXISTS (SELECT 1 FROM kill_state WHERE org_slug = 'default');

-- Outbox drafts (additive; reuse if already present from future level)
CREATE TABLE IF NOT EXISTS outbox_drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_slug VARCHAR(63) NOT NULL,
    target_url TEXT NOT NULL,
    body_sha256 VARCHAR(64) NOT NULL,
    state VARCHAR(31) NOT NULL DEFAULT 'DRAFT'  -- DRAFT | PENDING_APPROVAL | APPROVED | STALE | REJECTED | HANDED_OFF
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    approved_at TIMESTAMPTZ,
    expiry_at TIMESTAMPTZ,
    binding_sha256 VARCHAR(64),
    target_etag VARCHAR(255),
    target_state JSONB DEFAULT '{}',
    registry_policy_hash VARCHAR(64),
    kill_epoch_at_grant BIGINT,
    stale_reason TEXT
);
CREATE INDEX IF NOT EXISTS idx_outbox_org_state ON outbox_drafts(org_slug, state);
CREATE INDEX IF NOT EXISTS idx_outbox_target ON outbox_drafts(target_url);

-- Approval token binding (store verifier + binding; no raw bearer in events)
CREATE TABLE IF NOT EXISTS approval_tokens (
    token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    draft_id UUID NOT NULL REFERENCES outbox_drafts(id) ON DELETE CASCADE,
    binding_sha256 VARCHAR(64) NOT NULL,
    kill_epoch_at_grant BIGINT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(31) NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE | CONSUMED | INVALIDATED
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_approval_draft ON approval_tokens(draft_id);
CREATE INDEX IF NOT EXISTS idx_approval_expires ON approval_tokens(expires_at) WHERE status = 'ACTIVE';
