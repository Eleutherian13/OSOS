from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, HttpUrl


class PolicyValue(str, Enum):
    BLOCKED = "BLOCKED"
    ASSIST_ONLY = "ASSIST_ONLY"
    DISCLOSE = "DISCLOSE"
    ALLOWED = "ALLOWED"
    UNKNOWN = "UNKNOWN"


POLICY_SURFACES = [
    "proposal_text",
    "proposal_estimate",
    "code",
    "understanding_aid",
    "autonomous_agents",
    "comms_text",
]


class SourceRef(BaseModel):
    """Source provenance for a policy classification.
    A source ID must resolve; a valid URL and excerpt are required.
    Human confirmation (RegistryV21.human_confirmed) is required for the
    classification to be trusted; the source record alone does not approve it."""
    id: str = Field(min_length=1)
    url: HttpUrl
    excerpt: str = Field(min_length=1)
    sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    status: Literal["MONITORED", "PENDING_BASELINE", "UNVERIFIED"] = "PENDING_BASELINE"

    @field_validator("sha256", mode="before")
    @classmethod
    def check_hash(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and len(v) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in v):
            return v.lower()
        raise ValueError("sha256 must be 64 hex chars (lowercase); PENDING_BASELINE belongs in status")


class PolicySurfaceMap(BaseModel):
    proposal_text: PolicyValue = PolicyValue.UNKNOWN
    proposal_estimate: PolicyValue = PolicyValue.UNKNOWN
    code: PolicyValue = PolicyValue.UNKNOWN
    understanding_aid: PolicyValue = PolicyValue.UNKNOWN
    autonomous_agents: PolicyValue = PolicyValue.UNKNOWN
    comms_text: PolicyValue = PolicyValue.UNKNOWN


class ContactRules(BaseModel):
    channel: str = Field(min_length=1)
    direct_messages_welcome: bool = False
    quote: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)

    @field_validator("channel")
    @classmethod
    def channel_not_empty(cls, v: str) -> str:
        if v.strip() == "" or v.lower() == "unknown":
            raise ValueError("contact channel must be explicit; empty/unknown requires explicit representation")
        return v


class RegistryV21(BaseModel):
    organization_slug: str = Field(min_length=1, pattern=r"^[a-z0-9\-]+$")
    program: str = Field(min_length=1)
    version: Literal["2.1"] = "2.1"
    sources: list[SourceRef]
    policy: PolicySurfaceMap
    disclosure_required: bool = False
    contact: ContactRules
    human_confirmed: bool = False
    reconfirmation_needed: bool = False
    reconfirmation_reason: str = ""

    @field_validator("sources")
    @classmethod
    def distinct_source_ids(cls, v: list[SourceRef]) -> list[SourceRef]:
        ids = [s.id for s in v]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate source ids")
        return v
