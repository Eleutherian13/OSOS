"""Typed inputs for the deterministic Guard."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ActionClass = Literal["L0", "L1", "L2", "L3", "L4"]
GuardChoice = Literal["ALLOW", "NEEDS_HUMAN", "DENY"]


class BudgetStatus(BaseModel):
    """Typed budget-decision dependency (contract from Prompt 0)."""
    applicable: bool = False          # does this action consume budget?
    within_budget: bool | None = None  # None = unknown
    reason: str = ""


class ContactChannel(BaseModel):
    known: bool = False
    channel: str = ""                  # e.g. "DM", "public", "email"
    dm_permitted: bool = False


class RegistryContext(BaseModel):
    org_slug: str
    effective_mode: Literal["OBSERVE", "ASSIST_ONLY", "DISCLOSE", "ALLOWED", "UNKNOWN"] = "UNKNOWN"
    digest: str = ""                    # policy hash
    needs_reconfirm: bool = False
    fresh: bool = False                  # projection digest matches registry


class CapStatus(BaseModel):
    public_messages_this_week: int = 0
    max_public_messages_per_week: int = 3
    active_claims: int = 0
    max_active_claims: int = 1
    open_prs: int = 0
    max_open_prs: int = 2


class KillContext(BaseModel):
    epoch: int = 0
    expected_epoch: int = 0            # epoch operation expects
    source: Literal["db", "stop_file", "unknown"] = "unknown"


class GuardInput(BaseModel):
    action_class: ActionClass
    action_id: str = ""
    org_slug: str = ""
    registry: RegistryContext
    kill: KillContext
    caps: CapStatus = Field(default_factory=CapStatus)
    contact: ContactChannel = Field(default_factory=ContactChannel)
    budget: BudgetStatus = Field(default_factory=BudgetStatus)
