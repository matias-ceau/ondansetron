import sys
sys.path.append('.')
from mcp.tools import get_available_api_keys
import json

print(json.dumps(get_available_api_keys()))
