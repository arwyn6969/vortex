"""Serve a built VORTEX game locally, with no scientific or AI dependencies."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import webbrowser

class GameHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(403, "Directory listings are disabled")
        return None

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def main(argv=None):
    parser = argparse.ArgumentParser(description="Open VORTEX: the Nile of Rare Frogs")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--open", action="store_true", help="Open the game in your browser")
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent.parent / "dist")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    directory = args.directory.resolve()
    if not (directory / "index.html").is_file():
        print("Build the browser game first: npm ci && npm run build", file=sys.stderr)
        return 1
    try:
        with ThreadingHTTPServer(("127.0.0.1", args.port), partial(GameHandler, directory=str(directory))) as server:
            url = f"http://127.0.0.1:{args.port}/"
            print(f"VORTEX is ready: {url}\nPress Ctrl+C to close the local server.", flush=True)
            if args.open:
                webbrowser.open(url)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nThe Nile will be here when you return.")
    except OSError as error:
        print(f"Could not start the local server: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
