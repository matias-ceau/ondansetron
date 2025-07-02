import os
import requests

def get_available_api_keys():
    """
    Returns a list of available API keys from the environment variables.
    """
    api_keys = {}
    for key, value in os.environ.items():
        if 'API_KEY' in key.upper():
            api_keys[key] = value
    return api_keys

def perplexity_search(query):
    """
    Performs a search using the Perplexity API.
    """
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return {"error": "PERPLEXITY_API_KEY not found in environment variables."}

    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "pplx-7b-online",
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
