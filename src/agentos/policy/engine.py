from __future__ import annotations

from enum import Enum


class EffectiveMode(str, Enum):
    OBSERVE = "OBSERVE"
    UNDERSTANDING_ONLY = "UNDERSTANDING_ONLY"
    ASSIST = "ASSIST"
    COPILOT = "COPILOT"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_DISCLOSURE = "ALLOW_WITH_DISCLOSURE"
    ASSIST_ONLY = "ASSIST_ONLY"
    DENY = "DENY"
    UNKNOWN = "UNKNOWN"


class PolicyEngine:
    """Deterministic, pure policy evaluator — no LLM, no randomness."""

    @staticmethod
    def effective_mode(registry):
        """Derive ceiling operating mode from code + autonomous_agents + confirmation."""
        # Per Prompt 0 contract / v2.1 architecture:
        p = registry.policy
        confirmed = getattr(registry, "human_confirmed", False)
        reconfirm = getattr(registry, "reconfirmation_needed", False)

        # Conservative when unconfirmed / needs reconfirmation
        if not confirmed or reconfirm:
            # If code is BLOCKED or unknown and unconfirmed: conservative
            if p.code in ("BLOCKED", "UNKNOWN") or p.autonomous_agents == "BLOCKED":
                # Conservative floor when policy not fully established
                return EffectiveMode.OBSERVE

        # Core mapping (Prompt 0, item 6)
        # code BLOCKED -> UNDERSTANDING_ONLY (regardless of autonomous agents, per spec interpretation)
        if p.code == "BLOCKED":
            return EffectiveMode.UNDERSTANDING_ONLY

        # ASSIST_ONLY or DISCLOSE with autonomous BLOCKED/UNKNOWN -> ASSIST
        if p.code in ("ASSIST_ONLY", "DISCLOSE"):
            if p.autonomous_agents in ("BLOCKED", "UNKNOWN"):
                return EffectiveMode.ASSIST
            # If autonomous allowed — spec ambiguous; conservative = ASSIST (documented interpretation)
            return EffectiveMode.ASSIST

        # ALLOWED with autonomous BLOCKED/UNKNOWN -> COPILOT (spec says this explicitly)
        if p.code == "ALLOWED":
            if p.autonomous_agents in ("BLOCKED", "UNKNOWN"):
                return EffectiveMode.COPILOT
            if p.autonomous_agents == "ALLOWED":
                return EffectiveMode.COPILOT
            # autonomous_agents UNKNOWN but code ALLOWED -> COPILOT per explicit rule
            return EffectiveMode.COPILOT

        # Unknown policy -> conservative
        return EffectiveMode.OBSERVE

    @staticmethod
    def evaluate_surface(registry, surface: str, activity_context: str = "") -> dict:
        pval = getattr(registry.policy, surface, "UNKNOWN")
        # Disclosure preservation
        if pval == "DISCLOSE" or registry.disclosure_required:
            dec = Decision.ALLOW_WITH_DISCLOSURE if pval in ("ALLOWED", "DISCLOSE", "ASSIST_ONLY") else Decision.DENY
            # If DISCLOSE explicitly: preserve disclosure even if not allowed
            if pval == "DISCLOSE":
                dec = Decision.ALLOW_WITH_DISCLOSURE
            reason = f"surface {surface} = {pval}; disclosure_required={registry.disclosure_required}"
        elif pval == "BLOCKED":
            dec = Decision.DENY
            reason = f"surface {surface} explicitly BLOCKED"
        elif pval == "ASSIST_ONLY":
            dec = Decision.ASSIST_ONLY
            reason = f"surface {surface} = ASSIST_ONLY; no autonomous execution permitted"
        elif pval == "ALLOWED":
            dec = Decision.ALLOW
            reason = f"surface {surface} = ALLOWED"
        else:
            dec = Decision.UNKNOWN
            reason = f"surface {surface} = UNKNOWN; permission not established"

        # Fail-closed: unconfirmed / reconfirmation needed -> restrict
        if not getattr(registry, "human_confirmed", False) or getattr(registry, "reconfirmation_needed", False):
            if dec in (Decision.ALLOW, Decision.ALLOW_WITH_DISCLOSURE):
                dec = Decision.UNKNOWN
                reason += "; restricted because registry not confirmed / requires reconfirmation"

        return {
            "requested_surface": surface,
            "recorded_policy": pval,
            "decision": dec.value,
            "reason": reason,
            "source_refs": [s.id for s in getattr(registry, "sources", [])],
            "confirmation": getattr(registry, "human_confirmed", False),
            "reconfirmation": getattr(registry, "reconfirmation_needed", False),
        }
