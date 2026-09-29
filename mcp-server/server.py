from mcp.server.fastmcp import FastMCP

mcp = FastMCP("word-definition-server", host="0.0.0.0", port=8001)

DICTIONARY = {
    "authentication": "The process of verifying the identity of a user or system.",
    "authorization": "The process of determining what an authenticated user is allowed to do.",
    "encryption": "The process of converting data into a coded form to prevent unauthorized access.",
    "api": "A set of rules that allows different software applications to communicate with each other.",
    "database": "An organized collection of structured data stored electronically.",
    "token": "A piece of data used to verify identity or grant access, often used in authentication.",
    "embedding": "A numerical vector representation of text that captures its meaning.",
    "chunk": "A small piece of text split from a larger document for processing.",
}

@mcp.tool()
def get_word_definition(word: str) -> str:
    """Get the definition of an English word."""
    return DICTIONARY.get(word.lower(), f"No definition found for the word: {word}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")    