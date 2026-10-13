"""Local stdio MCP server; never print application output to stdout."""
import json
import os
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from store import TaskStore

mcp = FastMCP("Engineering Task Manager")
store = TaskStore(os.environ.get("TASK_DB", str(Path(__file__).parent / "data/tasks.db")))


@mcp.tool()
def create_task(title: str, description: str = "") -> dict:
    """Create an engineering task. Title is required and limited to 200 characters."""
    return store.create(title, description)


@mcp.tool()
def search_tasks(query: str = "", status: Literal["todo", "in_progress", "done"] | None = None,
                 limit: int = 20) -> list[dict]:
    """Search titles and descriptions literally. Return at most 100 tasks."""
    return store.search(query, status, limit)


@mcp.tool()
def update_task_status(task_id: int, status: Literal["todo", "in_progress", "done"]) -> dict:
    """Update an existing task's status; fails if the ID does not exist."""
    return store.update_status(task_id, status)


@mcp.resource("tasks://recent")
def recent_tasks() -> str:
    """Read the 20 most recently created engineering tasks."""
    return json.dumps(store.search(), indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
