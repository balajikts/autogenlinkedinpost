from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


HOST = "127.0.0.1"
PORT = 8000


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print(
            "\nCallback received:"
        )

        print(
            self.path
        )

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            b"""
            <html>
                <body>
                    <h2>LinkedIn OAuth Callback Server</h2>
                    <p>Callback received successfully.</p>
                </body>
            </html>
            """
        )

    def log_message(
        self,
        format,
        *args
    ):

        return


server = HTTPServer(
    (HOST, PORT),
    CallbackHandler
)

print(
    f"Callback server running at "
    f"http://{HOST}:{PORT}"
)

print(
    "Press CTRL+C to stop."
)

server.serve_forever()