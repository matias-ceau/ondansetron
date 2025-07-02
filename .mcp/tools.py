import os

def get_available_api_keys():
    """
    Returns a list of available API keys from the environment variables.
    """
    api_keys = {}
    for key, value in os.environ.items():
        if 'API_KEY' in key.upper():
            api_keys[key] = value
    return api_keys
