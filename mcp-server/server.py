import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("word-definition-server", host="0.0.0.0", port=8001)

@mcp.tool()
def get_word_defination(word: str) -> str:
    """Get the definition of an English word."""
    try:
        r = httpx.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}, timeout=10")
        r.raise_for_status()
        data = r.json()
        return data[0]["meanings"][0]["definitions"][0]["definition"]
    except Exception:
        return f"No definition found for the word: {word}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")