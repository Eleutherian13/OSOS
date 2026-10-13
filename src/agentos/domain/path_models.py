"""Level 2: Mentor Project Path domain models."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid


class PathState(str, Enum):
    WATCH = "WATCH"
    ENGAGED = "ENGAGED"
    ACTIVE = "ACTIVE"
    BACKUP = "BACKUP"
    DROPPED = "DROPPED"


VALID_TRANSITIONS = {
    PathState.WATCH: {PathState.ENGAGED},
    PathState.ENGAGED: {PathState.ACTIVE, PathState.BACKUP, PathState.DROPPED},
    PathState.ACTIVE: {PathState.BACKUP, PathState.DROPPED},
    PathState.BACKUP: {PathState.ENGAGED, PathState.DROPPED},
    PathState.DROPPED: set(),
}


class InteractionLevel(int, Enum):
    NO_INTERACTION = 0
    GENERIC_ACKNOWLEDGEMENT = 1
    TECHNICAL_QUESTION_ANSWERED = 2
    ARTIFACT_REVIEWED = 3
    PROJECT_SPECIFIC_GUIDANCE = 4
    EXPLICIT_ENCOURAGEMENT = 5
    PROJECT_DIRECTION_DISCUSSED = 6
    CLEAR_MENTOR_PROJECT_ALIGNMENT = 7


LEVEL_QUOTE_REQUIRED = {5, 6, 7}


class Path:
    """Mentor Project Path entity."""
    def __init__(
        self,
        id: uuid.UUID,
        org_id: uuid.UUID,
        project_id: uuid.UUID,
        mentor_id: Optional[uuid.UUID] = None,
        path_type: str = "other",
        path_slug: str = "",
        state: PathState = PathState.WATCH,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.org_id = org_id
        self.project_id = project_id
        self.mentor_id = mentor_id
        self.path_type = path_type
        self.path_slug = path_slug
        self.state = state
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def transition_to(self, new_state: PathState) -> bool:
        """Return True if transition is valid."""
        current = PathState(self.state.value) if isinstance(self.state, str) else self.state
        target = new_state if isinstance(new_state, PathState) else PathState(new_state)
        allowed = VALID_TRANSITIONS.get(current, set())
        return target in allowed


class Interaction:
    """Mentor interaction record."""
    def __init__(
        self,
        id: uuid.UUID,
        path_id: uuid.UUID,
        interaction_type: str,
        direction: str,
        level: int,
        link: str,
        channel: str = "UNKNOWN",
        quote: Optional[str] = None,
        summary: Optional[str] = None,
        occurred_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.path_id = path_id
        self.interaction_type = interaction_type
        self.direction = direction
        self.level = level
        self.link = link
        self.channel = channel
        self.quote = quote
        self.summary = summary
        self.occurred_at = occurred_at or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()

    def validate(self) -> list[str]:
        """Return list of validation errors."""
        errors = []
        if not 0 <= self.level <= 7:
            errors.append(f"level must be 0-7, got {self.level}")
        if not self.link or not self.link.strip():
            errors.append("link is required")
        if self.level >= 5 and not self.quote:
            errors.append(f"level {self.level} requires quote")
        if self.level >= 3 and not self.link:
            errors.append(f"level {self.level} requires artifact link")
        return errors


class Followup:
    """Follow-up task record."""
    def __init__(
        self,
        id: uuid.UUID,
        path_id: uuid.UUID,
        interaction_id: Optional[uuid.UUID] = None,
        state: str = "pending",
        due_at: Optional[datetime] = None,
        note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.path_id = path_id
        self.interaction_id = interaction_id
        self.state = state
        self.due_at = due_at
        self.note = note
        self.created_at = created_at or datetime.utcnow()
