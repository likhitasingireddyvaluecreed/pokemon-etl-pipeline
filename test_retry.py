from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from extract import create_session


class FailureHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Server received request")

        self.send_response(503)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            b'{"error": "Service temporarily unavailable"}'
        )

    def log_message(self, format, *args):
        pass


server = HTTPServer(("127.0.0.1", 8000), FailureHandler)

server_thread = Thread(
    target=server.serve_forever,
    daemon=True
)

server_thread.start()

print("Starting test server on port 8000...")

session = create_session()

try:
    response = session.get(
        "http://127.0.0.1:8000/test",
        timeout=10
    )

    print("Final status:", response.status_code)
    print("Final response:", response.text)

except Exception as e:
    print("Final exception:", type(e).__name__, e)

finally:
    server.shutdown()
    server.server_close()
    print("Test server stopped.")