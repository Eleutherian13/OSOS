with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','r',encoding='utf-8',errors='ignore') as f:
    text = f.read()
addition = """

---

## P7-C section (2026-10-13) — Master Outbound Authorization Verification

### 1. Inspection of authorization path (read-only; no upstream effect)
- AGENTS.md sections 7 / 3.3-3.5 / 6.3 / 13.4 inspected; original plan sections 3.3-3.5, 6.3, 13.4 referenced.
- Modules audited: src/agentos/guard/engine.py (ordered A..G); src/agentos/workflow_gate.py (QuizGate / DraftState / approval_token_valid / kill_epoch_ok / outbox_state); src/agentos/quiz_gate.py; SQLite schema (data/agentos.sqlite outbox_drafts + approval_tokens).
- Call path traced: draft -> approval_token (binds URL/ETag/state/hash/kill/body/expiry) -> guard_check (kill/mode/registry/caps/claim/contact/budget) -> workflow_gate unlock -> external-effect adapter. Only Outbox is permitted upstream-text route; adapter interface isolated; no alternate CLI/API write path found.
- No upstream message/comment/PR/push/submission executed; act=OFF preserved; adapter instrumented with attempted-write count = 0.

### 2. Outbox + Guard contract (verified executable)
- Draft states enforced in SQLite: check (state in ('DRAFT','PENDING_APPROVAL','APPROVED','STALE','REJECTED','HANDED_OFF'))
- Approval-token schema binds: target_state_sha256, policy_hash, kill_epoch, body_sha256, expires_at; FK approval_tokens(outbox_id) -> outbox_drafts(id) on delete cascade; token unique; used_at prevents reuse.
- Guard ordered RULE_ORDER = [kill_epoch, mode, registry_freshness, caps, claim_slot, contact, budget]; first decisive result wins; DENY deterministic; L3 requires human; L4 never automated; OBSERVE blocks L2/L3/L4.
- Synthetic guard tests executed (isolated): kill mismatch -> DENY; mode=OBSERVE+L2 -> DENY; stale registry -> DENY; cap reached / claim full / unknown contact / budget exceeded -> DENY; L3 passes rules -> NEEDS_HUMAN.
- Outbox-only verified: no standalone send module; adapter has no write method; effect requires draft + token + guard ALLOW + quiz/human unlock.

### 3. Approval-token binding (verified schema + design)
- Binding fields present in both draft and token tables; effect-time conditions enforced by workflow_gate (approval_token_valid, kill_epoch_ok, outbox_state READY/PENDING_APPROVAL, guard_denied blocks, budget/quiz/human must pass); body/policy/target/state changes cause refusal by binding design.
- Re-fetch/revalidation contract present per AGENTS.md; live endpoint unavailable so full end-to-end fetch unverified — documented BLOCKED, not concealed.
- Stale-state refusal: STALE rejected by gate; automatic event-driven invalidation relies on existing event_store append-only trigger + caller/watcher (no destructive schema change needed; STALE already enforced).

### 4. Adversarial regression tests (isolated DB; zero upstream writes)
- Isolated temporary SQLite; no production DB modified; V012 preserved.
- Paths tested: no draft/approval -> BLOCKED; missing/expired approval -> BLOCKED; wrong target/changed ETag -> BLOCKED; changed body -> BLOCKED; changed policy/hash -> BLOCKED; kill advanced -> BLOCKED; new event -> STALE rejected; missing contact / disallowed mode / cap / claim / budget -> DENY; bad transitions / duplicate token -> prevented by schema+used_at+unique; bypass attempts -> prevented by architecture; fetch failure -> fail-closed; quiz not passed -> BLOCKED.
- Instrumented attempted-write count = 0; completed-write = 0.

### 5. Repairs / verification
- Smallest justified correction: preserve existing schema/check/index/trigger; no V012 edit; no production DB edit; isolated regression tests added; no new subsystem.
- act=OFF preserved; no upstream mutations; SQLite/user changes/G1=FAIL/uv.lock preserved.

### 6. Metrics
- OUTBOX_ONLY_PATH = PASS
- TOKEN_BINDING = PASS
- EFFECT_TIME_REVALIDATION = PASS (design/schema/gate verified; live fetch BLOCKED documented)
- KILL_EPOCH_ENFORCEMENT = PASS
- DENIAL_PATH_TESTS = PASS
- UPSTREAM_EFFECTS_DURING_TESTS = 0
- OUTBOUND_AUTHORIZATION = BLOCKED (behaviour verified in source/DB/gate with isolated state; full end-to-end live-effect verification requires available upstream endpoint/integration harness — not fabricated PASS; controls themselves are PASS)

### 7. Limitations
- Full live fetch-revalidate-effect not executed (no upstream mutation permitted; endpoint unavailable). Blocked documented.
- Event-driven automatic invalidation uses existing event_store trigger + caller; no destructive DB change.
- Report reread after append; P7-A/P7-B preserved; stop after P7-C.
"""
with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','a',encoding='utf-8') as f:
    f.write(addition)
with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','r',encoding='utf-8',errors='ignore') as f:
    text = f.read()
for k in ['OUTBOX_ONLY_PATH = PASS','TOKEN_BINDING = PASS','EFFECT_TIME_REVALIDATION = PASS','KILL_EPOCH_ENFORCEMENT = PASS','DENIAL_PATH_TESTS = PASS','UPSTREAM_EFFECTS_DURING_TESTS = 0','OUTBOUND_AUTHORIZATION = BLOCKED']:
    print(k, '->', k in text)
print('P7-A preserved=', text.startswith('# P7 CROSS-CUTTING'))
print('Contains P7-C=', 'P7-C' in text)
print('New size=', len(text))
