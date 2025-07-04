"""Script to run the FastMCP server using uv run."""

# Import the MCP instance from the module
from . import start_server

fastmcp = start_server()
mcp = fastmcp

if __name__ == "__main__":
    fastmcp.run()
