"""Level 2: Path and Interaction repositories (SQLite)."""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Iterable, Optional

from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection, Session
from agentos.domain.path_models import (
    Followup, Interaction, Path, PathState,
)


class PathRepo:
    """Persistence layer for paths."""

    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._config = connection.config if isinstance(connection, Connection) else connection
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def add(self, path: Path) -> Path:
        with Session(self._connection) as conn:
            conn.execute(
                """INSERT INTO paths (id, org_id, project_id, mentor_id, path_type, path_slug, state, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(path.id), str(path.org_id), str(path.project_id),
                    str(path.mentor_id) if path.mentor_id else None,
                    path.path_type, path.path_slug, path.state.value,
                    path.created_at.isoformat(), path.updated_at.isoformat(),
                ),
            )
        return path

    def get(self, path_id: uuid.UUID) -> Optional[Path]:
        rows = self._connection.fetchall(
            "SELECT id, org_id, project_id, mentor_id, path_type, path_slug, state, created_at, updated_at FROM paths WHERE id=?",
            (str(path_id),),
        )
        if not rows:
            return None
        row = rows[0]
        return Path(
            id=uuid.UUID(row["id"]),
            org_id=uuid.UUID(row["org_id"]),
            project_id=uuid.UUID(row["project_id"]),
            mentor_id=uuid.UUID(row["mentor_id"]) if row["mentor_id"] else None,
            path_type=row["path_type"],
            path_slug=row["path_slug"],
            state=PathState(row["state"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def list_all(self) -> list[Path]:
        rows = self._connection.fetchall("SELECT * FROM paths ORDER BY created_at DESC")
        return [
            Path(
                id=uuid.UUID(r["id"]),
                org_id=uuid.UUID(r["org_id"]),
                project_id=uuid.UUID(r["project_id"]),
                mentor_id=uuid.UUID(r["mentor_id"]) if r["mentor_id"] else None,
                path_type=r["path_type"],
                path_slug=r["path_slug"],
                state=PathState(r["state"]),
                created_at=datetime.fromisoformat(r["created_at"]),
                updated_at=datetime.fromisoformat(r["updated_at"]),
            )
            for r in rows
        ]

    def transition(self, path_id: uuid.UUID, new_state: PathState) -> Optional[Path]:
        """Return new Path if transition succeeds, None if invalid."""
        path = self.get(path_id)
        if not path:
            return None
        if not path.transition_to(new_state):
            return None
        path.state = new_state
        path.updated_at = datetime.utcnow()
        with Session(self._connection) as conn:
            conn.execute(
                """UPDATE paths SET state=?, updated_at=? WHERE id=?""",
                (new_state.value, path.updated_at.isoformat(), str(path_id)),
            )
        return path


class InteractionRepo:
    """Persistence layer for interactions."""

    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def add(self, interaction: Interaction) -> Interaction:
        with Session(self._connection) as conn:
            conn.execute(
                """INSERT INTO interactions (id, path_id, interaction_type, direction, level, link, channel, quote, summary, occurred_at, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(interaction.id), str(interaction.path_id),
                    interaction.interaction_type, interaction.direction,
                    interaction.level, interaction.link, interaction.channel,
                    interaction.quote, interaction.summary,
                    interaction.occurred_at.isoformat(), interaction.created_at.isoformat(),
                ),
            )
        return interaction

    def get(self, interaction_id: uuid.UUID) -> Optional[Interaction]:
        rows = self._connection.fetchall(
            "SELECT * FROM interactions WHERE id=?",
            (str(interaction_id),),
        )
        if not rows:
            return None
        row = rows[0]
        return Interaction(
            id=uuid.UUID(row["id"]),
            path_id=uuid.UUID(row["path_id"]),
            interaction_type=row["interaction_type"],
            direction=row["direction"],
            level=row["level"],
            link=row["link"],
            channel=row["channel"],
            quote=row["quote"],
            summary=row["summary"],
            occurred_at=datetime.fromisoformat(row["occurred_at"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_for_path(self, path_id: uuid.UUID) -> list[Interaction]:
        rows = self._connection.fetchall(
            "SELECT * FROM interactions WHERE path_id=? ORDER BY occurred_at DESC",
            (str(path_id),),
        )
        return [
            Interaction(
                id=uuid.UUID(r["id"]),
                path_id=uuid.UUID(r["path_id"]),
                interaction_type=r["interaction_type"],
                direction=r["direction"],
                level=r["level"],
                link=r["link"],
                channel=r["channel"],
                quote=r["quote"],
                summary=r["summary"],
                occurred_at=datetime.fromisoformat(r["occurred_at"]),
                created_at=datetime.fromisoformat(r["created_at"]),
            )
            for r in rows
        ]

    def get_max_level(self, path_id: uuid.UUID) -> int:
        rows = self._connection.fetchall(
            "SELECT MAX(level) as max_level FROM interactions WHERE path_id=?",
            (str(path_id),),
        )
        if rows and rows[0]["max_level"] is not None:
            return int(rows[0]["max_level"])
        return 0


class FollowupRepo:
    """Persistence layer for followups."""

    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def add(self, followup: Followup) -> Followup:
        with Session(self._connection) as conn:
            conn.execute(
                """INSERT INTO followups (id, path_id, interaction_id, state, due_at, note, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(followup.id), str(followup.path_id),
                    str(followup.interaction_id) if followup.interaction_id else None,
                    followup.state, followup.due_at.isoformat(),
                    followup.note, followup.created_at.isoformat(),
                ),
            )
        return followup

    def get(self, followup_id: uuid.UUID) -> Optional[Followup]:
        rows = self._connection.fetchall(
            "SELECT * FROM followups WHERE id=?",
            (str(followup_id),),
        )
        if not rows:
            return None
        row = rows[0]
        return Followup(
            id=uuid.UUID(row["id"]),
            path_id=uuid.UUID(row["path_id"]),
            interaction_id=uuid.UUID(row["interaction_id"]) if row["interaction_id"] else None,
            state=row["state"],
            due_at=datetime.fromisoformat(row["due_at"]),
            note=row["note"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_for_path(self, path_id: uuid.UUID) -> list[Followup]:
        rows = self._connection.fetchall(
            "SELECT * FROM followups WHERE path_id=? ORDER BY due_at ASC",
            (str(path_id),),
        )
        return [
            Followup(
                id=uuid.UUID(r["id"]),
                path_id=uuid.UUID(r["path_id"]),
                interaction_id=uuid.UUID(r["interaction_id"]) if r["interaction_id"] else None,
                state=r["state"],
                due_at=datetime.fromisoformat(r["due_at"]),
                note=r["note"],
                created_at=datetime.fromisoformat(r["created_at"]),
            )
            for r in rows
        ]

    def list_pending(self, path_id: uuid.UUID) -> list[Followup]:
        rows = self._connection.fetchall(
            "SELECT * FROM followups WHERE path_id=? AND state='pending' AND due_at > datetime('now') ORDER BY due_at ASC",
            (str(path_id),),
        )
        return [
            Followup(
                id=uuid.UUID(r["id"]),
                path_id=uuid.UUID(r["path_id"]),
                interaction_id=uuid.UUID(r["interaction_id"]) if r["interaction_id"] else None,
                state=r["state"],
                due_at=datetime.fromisoformat(r["due_at"]),
                note=r["note"],
                created_at=datetime.fromisoformat(r["created_at"]),
            )
            for r in rows
        ]

    def ensure_no_duplicate(self, path_id: uuid.UUID, interaction_id: uuid.UUID) -> bool:
        """Check if a followup already exists for this interaction."""
        rows = self._connection.fetchall(
            "SELECT 1 FROM followups WHERE path_id=? AND interaction_id=?",
            (str(path_id), str(interaction_id)),
        )
        return len(rows) == 0


class PathMentorRepo:
    """Persistence layer for the path-mentor relationship."""

    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def associate(self, path_id: uuid.UUID, mentor_id: uuid.UUID) -> bool:
        """Associate a mentor with a path (insert or ignore duplicate)."""
        import uuid
        self._connection.execute(
            "INSERT OR IGNORE INTO path_mentors (id, path_id, mentor_id, joined_at) VALUES (?, ?, ?, datetime('now'))",
            (str(uuid.uuid4()), str(path_id), str(mentor_id)),
        )
        rows = self._connection.fetchall(
            "SELECT 1 FROM path_mentors WHERE path_id=? AND mentor_id=?",
            (str(path_id), str(mentor_id)),
        )
        return len(rows) == 1

    def remove(self, path_id: uuid.UUID, mentor_id: uuid.UUID) -> bool:
        """Remove a mentor from a path. Returns True if a row was removed."""
        # Check existence first to distinguish "not present" from "deleted"
        before = self._connection.fetchall(
            "SELECT 1 FROM path_mentors WHERE path_id=? AND mentor_id=?",
            (str(path_id), str(mentor_id)),
        )
        self._connection.execute(
            "DELETE FROM path_mentors WHERE path_id=? AND mentor_id=?",
            (str(path_id), str(mentor_id)),
        )
        return len(before) > 0
