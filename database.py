"""SQLite veritabanı yönetimi — mülakat simülasyonu."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional


@dataclass(frozen=True)
class Interview:
    id: int
    user_name: str
    job_title: str
    date: str


@dataclass(frozen=True)
class Message:
    id: int
    interview_id: int
    role: str
    content: str


@dataclass(frozen=True)
class ScoreRow:
    id: int
    interview_id: int
    criterion: str
    score: float


class DatabaseManager:
    """Mülakat, mesaj ve puan kayıtları için SQLite yöneticisi."""

    def __init__(self, db_path: str | Path) -> None:
        self._path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def session(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        with self.session() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS interviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    date TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interview_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (interview_id)
                        REFERENCES interviews (id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_interview
                    ON messages (interview_id);

                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interview_id INTEGER NOT NULL,
                    criterion TEXT NOT NULL,
                    score REAL NOT NULL,
                    FOREIGN KEY (interview_id)
                        REFERENCES interviews (id)
                        ON DELETE CASCADE,
                    UNIQUE (interview_id, criterion)
                );

                CREATE INDEX IF NOT EXISTS idx_scores_interview
                    ON scores (interview_id);
                """
            )

    def create_interview(
        self,
        user_name: str,
        job_title: str,
        date: str,
        *,
        conn: Optional[sqlite3.Connection] = None,
    ) -> int:
        """Yeni mülakat kaydı; `date` ISO-8601 string (örn. 2025-03-22) önerilir."""
        sql = (
            "INSERT INTO interviews (user_name, job_title, date) "
            "VALUES (?, ?, ?)"
        )
        if conn is not None:
            cur = conn.execute(sql, (user_name, job_title, date))
            return int(cur.lastrowid)
        with self.session() as c:
            cur = c.execute(sql, (user_name, job_title, date))
            return int(cur.lastrowid)

    def add_message(
        self,
        interview_id: int,
        role: str,
        content: str,
        *,
        conn: Optional[sqlite3.Connection] = None,
    ) -> int:
        """role: örn. 'user', 'assistant', 'system'."""
        sql = (
            "INSERT INTO messages (interview_id, role, content) "
            "VALUES (?, ?, ?)"
        )
        if conn is not None:
            cur = conn.execute(sql, (interview_id, role, content))
            return int(cur.lastrowid)
        with self.session() as c:
            cur = c.execute(sql, (interview_id, role, content))
            return int(cur.lastrowid)

    def add_score(
        self,
        interview_id: int,
        criterion: str,
        score: float,
        *,
        conn: Optional[sqlite3.Connection] = None,
    ) -> int:
        """Aynı mülakatta aynı kriter tekrarlanırsa kayıt güncellenir."""
        sql = (
            "INSERT INTO scores (interview_id, criterion, score) VALUES (?, ?, ?) "
            "ON CONFLICT(interview_id, criterion) DO UPDATE SET score = excluded.score"
        )
        if conn is not None:
            cur = conn.execute(sql, (interview_id, criterion, score))
            return int(cur.lastrowid)
        with self.session() as c:
            cur = c.execute(sql, (interview_id, criterion, score))
            return int(cur.lastrowid)

    def get_interview(self, interview_id: int) -> Optional[Interview]:
        with self.session() as conn:
            row = conn.execute(
                "SELECT id, user_name, job_title, date FROM interviews WHERE id = ?",
                (interview_id,),
            ).fetchone()
        if row is None:
            return None
        return Interview(
            id=row["id"],
            user_name=row["user_name"],
            job_title=row["job_title"],
            date=row["date"],
        )

    def list_messages(self, interview_id: int) -> list[Message]:
        with self.session() as conn:
            rows = conn.execute(
                "SELECT id, interview_id, role, content FROM messages "
                "WHERE interview_id = ? ORDER BY id ASC",
                (interview_id,),
            ).fetchall()
        return [
            Message(
                id=r["id"],
                interview_id=r["interview_id"],
                role=r["role"],
                content=r["content"],
            )
            for r in rows
        ]

    def list_scores(self, interview_id: int) -> list[ScoreRow]:
        with self.session() as conn:
            rows = conn.execute(
                "SELECT id, interview_id, criterion, score FROM scores "
                "WHERE interview_id = ? ORDER BY criterion ASC",
                (interview_id,),
            ).fetchall()
        return [
            ScoreRow(
                id=r["id"],
                interview_id=r["interview_id"],
                criterion=r["criterion"],
                score=float(r["score"]),
            )
            for r in rows
        ]

    def list_interviews(self, limit: int = 100) -> list[Interview]:
        with self.session() as conn:
            rows = conn.execute(
                "SELECT id, user_name, job_title, date FROM interviews "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            Interview(
                id=r["id"],
                user_name=r["user_name"],
                job_title=r["job_title"],
                date=r["date"],
            )
            for r in rows
        ]

    def delete_interview(self, interview_id: int) -> None:
        with self.session() as conn:
            conn.execute("DELETE FROM interviews WHERE id = ?", (interview_id,))
