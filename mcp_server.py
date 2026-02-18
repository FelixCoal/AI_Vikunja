import os

from mcp.server.fastmcp import FastMCP

from task_service import create_task_from_text

mcp = FastMCP("ai-vikunja", stateless_http=True, json_response=True)


@mcp.tool(name="add_task")
def add_task(text: str) -> dict:
    task = create_task_from_text(text)
    return task.model_dump()


if __name__ == "__main__":
    mcp.settings.host = os.getenv("MCP_HOST", "0.0.0.0")
    mcp.settings.port = int(os.getenv("MCP_PORT", "8001"))
    mcp.run(transport="streamable-http")
