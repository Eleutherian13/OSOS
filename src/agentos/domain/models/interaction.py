from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone

class Interaction(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    path_id: uuid.UUID
    direction: Literal["inbound","outbound"]
    level: int = Field(ge=0, le=7)
    link: str = Field(min_length=1)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quote: str | None = None
    note: str | None = None

class Followup(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    path_id: uuid.UUID
    interaction_id: uuid.UUID | None = None
    state: Literal["pending","completed","cancelled"] = "pending"
    due_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
