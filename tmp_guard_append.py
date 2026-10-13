# Prompt 3 integrity guard — appended block (AGENTS.md §9 F / §6 / §7)
    def confirm_requires_maintainer_reply(self, record, reply_evidence_ref: str, reply_ts: str) -> bool:
        if not reply_evidence_ref or not reply_ts:
            return False
        return (record.author_role == "maintainer") or reply_evidence_ref.startswith("maintainer:")
    def forbidden_claims_check(self, result: dict) -> bool:
        for bad in ("FREE", "AVAILABLE"):
            if bad in (result.get("reason") or "") or bad == result.get("proposed_state"):
                return False
        return result.get("no_free_assertion") is True
