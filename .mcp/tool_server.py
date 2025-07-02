from mcp.server.fastmcp import FastMCP
import os
import requests

# Create an MCP server
mcp = FastMCP("Ondansetron Project Tools")

@mcp.tool()
def get_available_api_keys() -> dict:
    """
    Returns a list of available API keys from the environment variables.
    """
    api_keys = {}
    for key, value in os.environ.items():
        if 'API_KEY' in key.upper():
            api_keys[key] = value
    return api_keys

@mcp.tool()
def perplexity_search(query: str) -> dict:
    """
    Performs a search using the Perplexity API.
    """
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return {"error": "PERPLEXITY_API_KEY not found in environment variables."}

    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3-sonar-large-32k-online",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and factual."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    mcp.run()
