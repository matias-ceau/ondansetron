import http.server
import socketserver
import json
import os
from tools import get_available_api_keys, perplexity_search

PORT = 8000

class ToolServer(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/run_tool':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            tool_request = json.loads(post_data)

            tool_name = tool_request.get('tool_name')
            tool_params = tool_request.get('tool_params')

            if tool_name == 'get_available_api_keys':
                result = get_available_api_keys()
                response = {
                    "status": "success",
                    "result": result
                }
            elif tool_name == 'perplexity_search':
                query = tool_params.get('query')
                if query:
                    result = perplexity_search(query)
                    response = {
                        "status": "success",
                        "result": result
                    }
                else:
                    response = {
                        "status": "error",
                        "message": "Missing 'query' parameter for perplexity_search."
                    }
            else:
                response = {
                    "status": "error",
                    "message": f"Tool '{tool_name}' not found."
                }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

with socketserver.TCPServer(("", PORT), ToolServer) as httpd:
    print("Tool server listening on port", PORT)
    httpd.serve_forever()
