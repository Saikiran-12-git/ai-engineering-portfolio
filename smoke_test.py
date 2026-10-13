"""Exercise real MCP initialization, tool discovery and tool calls over stdio."""
import asyncio
import os
import sys
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, TASK_DB=str(Path(tmp) / "tasks.db"))
        params = StdioServerParameters(command=sys.executable,
            args=[str(Path(__file__).with_name("server.py"))], env=env)
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                names = {tool.name for tool in (await client.list_tools()).tools}
                assert names == {"create_task", "search_tasks", "update_task_status"}
                created = await client.call_tool("create_task", {"title": "Review Java upgrade"})
                assert not created.isError
                found = await client.call_tool("search_tasks", {"query": "Java"})
                assert not found.isError and "Review Java upgrade" in str(found.content)
                bad = await client.call_tool("update_task_status", {"task_id": 999, "status": "done"})
                assert bad.isError
                resource = await client.read_resource("tasks://recent")
                assert "Review Java upgrade" in str(resource.contents)
    print("MCP protocol smoke test passed")


if __name__ == "__main__":
    asyncio.run(main())
