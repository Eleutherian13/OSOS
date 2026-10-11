from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal
import uuid
from datetime import datetime, timezone

class Organization(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=63)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Project(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    org_id: uuid.UUID
    title: str
    slug: str = Field(min_length=1, max_length=63)
    repo_url: str | None = None
    description: str | None = None

class Mentor(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    org_id: uuid.UUID
    handle: str
    contact_channel_hint: str | None = None

class PathState:
    WATCH = "WATCH"
    ENGAGED = "ENGAGED"
    ACTIVE = "ACTIVE"
    BACKUP = "BACKUP"
    DROPPED = "DROPPED"
    VALUES = {WATCH, ENGAGED, ACTIVE, BACKUP, DROPPED}

class Prerequisite(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    path_id: uuid.UUID
    title: str
    resolved: bool = False

class Path(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    org_id: uuid.UUID
    project_id: uuid.UUID
    state: Literal["WATCH","ENGAGED","ACTIVE","BACKUP","DROPPED"] = "WATCH"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
