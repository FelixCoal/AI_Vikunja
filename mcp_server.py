from mcp.server.fastmcp import FastMCP

from task_service import create_task_from_text

mcp = FastMCP("ai-vikunja")


@mcp.tool(name="add_task")
def add_task(text: str) -> dict:
    task = create_task_from_text(text)
    return task.model_dump()


if __name__ == "__main__":
    mcp.run()
