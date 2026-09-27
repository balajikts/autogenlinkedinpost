import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from linkedin.auth import build_authorization_url, exchange_code_for_token

HOST = "127.0.0.1"
PORT = 8000
TOKEN_FILE = ".linkedin_token.json"


class OAuthCallbackHandler(BaseHTTPRequestHandler):

    expected_state = None
    server = None

    def do_GET(self):

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/auth/linkedin/callback":
            self.send_error(404, "Invalid callback path")
            return

        params = parse_qs(parsed_url.query)

        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        error = params.get("error", [None])[0]

        # Handle LinkedIn authorization errors
        if error:
            self.send_html(
                f"<h2>LinkedIn authorization failed</h2>"
                f"<p>Error: {error}</p>"
            )
            self.server.shutdown()
            return

        # Validate state
        if not state or state != self.expected_state:
            self.send_html(
                "<h2>Security validation failed</h2>"
                "<p>Invalid OAuth state.</p>"
            )
            self.server.shutdown()
            return

        if not code:
            self.send_html(
                "<h2>Authorization failed</h2>"
                "<p>No authorization code received.</p>"
            )
            self.server.shutdown()
            return

        try:
            token_data = exchange_code_for_token(code)

            with open(TOKEN_FILE, "w", encoding="utf-8") as file:
                json.dump(token_data, file, indent=2)

            self.send_html(
                "<h2>LinkedIn authorization successful!</h2>"
                "<p>You can close this browser window.</p>"
            )

            print("\n✅ LinkedIn authorization successful.")
            print(f"✅ Token saved to {TOKEN_FILE}")

        except Exception as exc:
            print("\n❌ Token exchange failed.")
            print(f"Error: {exc}")

            self.send_html(
                "<h2>LinkedIn authorization failed</h2>"
                "<p>Token exchange failed. Check the terminal.</p>"
            )

        finally:
            self.server.shutdown()

    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        response = f"""
        <html>
            <body style="font-family: Arial; padding: 40px;">
                {html}
            </body>
        </html>
        """

        self.wfile.write(response.encode("utf-8"))

    def log_message(self, format, *args):
        return


def login():

    authorization_url, state = build_authorization_url()

    OAuthCallbackHandler.expected_state = state

    server = HTTPServer(
        (HOST, PORT),
        OAuthCallbackHandler
    )

    OAuthCallbackHandler.server = server

    print("\n========================================")
    print(" LinkedIn OAuth Login")
    print("========================================")

    print("\nOpening LinkedIn authorization page...")

    print("\nIf the browser does not open automatically,")
    print("open this URL manually:\n")

    print(authorization_url)

    webbrowser.open(authorization_url)

    print("\nWaiting for LinkedIn callback...")
    print(f"Callback: http://{HOST}:{PORT}/auth/linkedin/callback")

    server.serve_forever()

    server.server_close()

    print("\nOAuth process completed.")


if __name__ == "__main__":
    login()