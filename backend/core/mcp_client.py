from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client as streamable_http_client

MCP_URL = "http://localhost:8001/mcp"

async def call_word_definition(word: str) -> str:
    async with streamable_http_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_word_definition", {"word": word})
            return result.content[0].text