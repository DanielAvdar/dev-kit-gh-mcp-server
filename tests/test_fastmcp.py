from pathlib import Path

import pytest
from fastmcp import Client

from dev_kit_gh_mcp_server import start_server
from dev_kit_gh_mcp_server.tools import __all__


@pytest.fixture
def fastmcp_server(temp_dir):
    """Fixture to start the FastMCP server."""
    with open(Path(__file__).parent / "Makefile", "r") as f:
        make_content = f.read()
    with open(Path(temp_dir) / "Makefile", "w") as f:
        f.write(make_content)
    server = start_server(temp_dir)

    return server


@pytest.mark.asyncio
async def test_tool_with_client(fastmcp_server):
    # Pass the server directly to the Client constructor
    async with Client(fastmcp_server) as client:
        result = await client.list_tools()
        assert len(result) == len(__all__)
