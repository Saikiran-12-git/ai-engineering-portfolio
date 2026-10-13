"""Transactional task storage. No model or MCP dependency."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

STATUSES = {"todo", "in_progress", "done"}


class TaskStore:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, title TEXT NOT NULL,
                description TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'todo'
                CHECK(status IN ('todo','in_progress','done')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def create(self, title, description=""):
        title = title.strip()
        if not title or len(title) > 200:
            raise ValueError("Title must contain 1–200 characters")
        if len(description) > 10000:
            raise ValueError("Description exceeds 10000 characters")
        with self.connection() as conn:
            task_id = conn.execute(
                "INSERT INTO tasks(title, description) VALUES (?, ?)",
                (title, description),
            ).lastrowid
            return dict(conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())

    def search(self, query="", status=None, limit=20):
        if status is not None and status not in STATUSES:
            raise ValueError("Invalid status")
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")
        if len(query) > 500:
            raise ValueError("Query exceeds 500 characters")
        # instr uses literal matching: %, _, and SQL-like text are not operators.
        with self.connection() as conn:
            return [dict(row) for row in conn.execute(
                """SELECT * FROM tasks WHERE
                (instr(lower(title), lower(?)) > 0 OR instr(lower(description), lower(?)) > 0)
                AND (? IS NULL OR status=?) ORDER BY id DESC LIMIT ?""",
                (query, query, status, status, limit),
            )]

    def update_status(self, task_id, status):
        if status not in STATUSES:
            raise ValueError("Invalid status")
        with self.connection() as conn:
            result = conn.execute(
                "UPDATE tasks SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (status, task_id),
            )
            if not result.rowcount:
                raise ValueError("Task not found")
            return dict(conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())
