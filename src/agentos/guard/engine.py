"""Deterministic Guard evaluation — pure, ordered, typed."""
from __future__ import annotations

from .types import (
    ActionClass,
    GuardChoice,
    GuardInput,
)

# Ordered rule labels (must match spec A..G)
RULE_ORDER = ["kill_epoch", "mode", "registry_freshness", "caps", "claim_slot", "contact", "budget"]


def allow(action_id: str = "", reasons: list[str] | None = None) -> dict:
    return {"decision": "ALLOW", "action_id": action_id, "reasons": reasons or [], "missing": []}


def deny(action_id: str = "", reasons: list[str] | None = None, missing: list[str] | None = None) -> dict:
    return {"decision": "DENY", "action_id": action_id, "reasons": reasons or [], "missing": missing or []}


def needs_human(action_id: str = "", reasons: list[str] | None = None, missing: list[str] | None = None) -> dict:
    return {"decision": "NEEDS_HUMAN", "action_id": action_id, "reasons": reasons or [], "missing": missing or []}


def _mode_decision(action: ActionClass, mode: str) -> GuardChoice | None:
    if action == "L4":
        return "DENY"  # never automated
    if action == "L3":
        return "NEEDS_HUMAN"  # must require explicit human approval + execution
    # L0/L1/L2 proceed if mode permits (handled below)
    if mode == "OBSERVE" and action in ("L2", "L3", "L4"):
        return "DENY" if action == "L4" else "DENY"  # conservative: observe blocks action
    return None  # continue


def guard_check(inp: GuardInput) -> dict:
    """Ordered evaluation A..G. First decisive result wins."""
    res = {
        "decision": "ALLOW",
        "action_id": inp.action_id,
        "action_class": inp.action_class,
        "org_slug": inp.org_slug,
        "rules_evaluated": [],
        "reasons": [],
        "missing": [],
        "source_refs": [],
    }
    evaluated: list[str] = []

    # A. Kill epoch
    evaluated.append("kill_epoch")
    if inp.kill.epoch != inp.kill.expected_epoch or inp.kill.source == "unknown":
        if inp.kill.source == "unknown":
            res.update(deny(inp.action_id, ["kill_epoch_unknown_source"], ["kill_epoch"]))
        else:
            res.update(deny(inp.action_id, [f"kill_epoch_mismatch: current={inp.kill.epoch} expected={inp.kill.expected_epoch}"], ["kill_epoch"]))
        res["rules_evaluated"] = evaluated
        return res
    res["reasons"].append("kill_epoch_ok")

    # B. Mode
    evaluated.append("mode")
    mode_result = _mode_decision(inp.action_class, inp.registry.effective_mode)
    if mode_result is not None:
        if mode_result == "DENY":
            res.update(deny(inp.action_id, [f"mode_denied: {inp.action_class} with mode={inp.registry.effective_mode}"]))
        elif mode_result == "NEEDS_HUMAN":
            res.update(needs_human(inp.action_id, [f"mode_requires_human: {inp.action_class} (L3 requires explicit human approval/execution)"], []))
        res["rules_evaluated"] = evaluated
        res["reasons"].append("mode_decisive")
        return res
    if inp.registry.effective_mode == "UNKNOWN":
        res.update(deny(inp.action_id, ["mode_unknown"], ["effective_mode"]))
        res["rules_evaluated"] = evaluated
        return res
    res["reasons"].append(f"mode_ok:{inp.registry.effective_mode}")

    # C. Registry freshness / reconfirm
    evaluated.append("registry_freshness")
    if not inp.registry.fresh or inp.registry.needs_reconfirm:
        if inp.registry.needs_reconfirm:
            res.update(deny(inp.action_id, ["registry_needs_reconfirm"], ["registry_freshness"]))
        else:
            res.update(deny(inp.action_id, ["registry_stale"], ["registry_freshness"]))
        res["rules_evaluated"] = evaluated
        return res
    res["reasons"].append("registry_fresh_ok")

    # D. Caps (only relevant caps)
    evaluated.append("caps")
    caps = inp.caps
    if inp.action_class == "L3" and caps.public_messages_this_week >= caps.max_public_messages_per_week:
        res.update(deny(inp.action_id, ["public_message_cap_reached"], ["caps"]))
        res["rules_evaluated"] = evaluated
        return res
    res["reasons"].append("caps_ok")

    # E. Active claim slot
    evaluated.append("claim_slot")
    if inp.action_class == "L3" and caps.active_claims >= caps.max_active_claims:
        res.update(deny(inp.action_id, ["active_claim_limit_reached"], ["claim_slot"]))
        res["rules_evaluated"] = evaluated
        return res
    res["reasons"].append("claim_slot_ok")

    # F. Contact channel
    evaluated.append("contact")
    if inp.action_class in ("L2", "L3", "L4"):
        if not inp.contact.known:
            res.update(deny(inp.action_id, ["contact_channel_unknown"], ["contact"]))
            res["rules_evaluated"] = evaluated
            return res
        if inp.contact.channel == "DM" and not inp.contact.dm_permitted:
            res.update(deny(inp.action_id, ["dm_not_permitted"], ["contact"]))
            res["rules_evaluated"] = evaluated
            return res
        if inp.action_class == "L3" and inp.contact.channel not in ("public", "DM", "email", "forum"):
            # still require a known channel; unknown string treated as unknown
            pass
    res["reasons"].append("contact_ok")

    # G. Budget eligibility (typed dependency)
    evaluated.append("budget")
    if inp.budget.applicable:
        if inp.budget.within_budget is None:
            res.update(deny(inp.action_id, ["budget_unknown"], ["budget"]))
            res["rules_evaluated"] = evaluated
            return res
        if not inp.budget.within_budget:
            res.update(deny(inp.action_id, ["budget_exceeded"], ["budget"]))
            res["rules_evaluated"] = evaluated
            return res
    res["reasons"].append("budget_ok_or_neutral")

    # All rules passed
    res["rules_evaluated"] = evaluated
    # L3 needs human approval — must return NEEDS_HUMAN even when all rules pass
    if inp.action_class == "L3":
        res.update(needs_human(inp.action_id, ["L3_requires_explicit_human_approval_and_execution"], []))
        return res
    # L4 never allowed (already handled in mode, but double-check conservative)
    if inp.action_class == "L4":
        res.update(deny(inp.action_id, ["L4_never_automated"], []))
        return res
    res.update(allow(inp.action_id, res["reasons"]))
    return res
