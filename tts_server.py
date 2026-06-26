#!/usr/bin/env python3
"""TTS micro-server for The Questionarium — edge-tts Andrew voice, on demand.
Run this in the background: python tts_server.py
The game auto-detects it at http://localhost:8942 and switches to Andrew's voice."""

import asyncio, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from io import BytesIO
import tempfile, os, hashlib, time

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import edge_tts

VOICE = "en-US-AndrewNeural"
PORT = 8942
CACHE = {}  # text_hash -> (mp3_bytes, timestamp)
CACHE_MAX = 200
CACHE_TTL = 3600  # 1 hour


def cache_key(text):
    return hashlib.md5(text.encode()).hexdigest()


async def generate_audio(text):
    """Generate MP3 for the given text, cached."""
    key = cache_key(text)
    now = time.time()

    # Prune old entries
    stale = [k for k, v in CACHE.items() if now - v[1] > CACHE_TTL]
    for k in stale:
        del CACHE[k]

    # Prune by count
    if len(CACHE) > CACHE_MAX:
        oldest = sorted(CACHE.items(), key=lambda x: x[1][1])[:len(CACHE) - CACHE_MAX]
        for k, _ in oldest:
            del CACHE[k]

    if key in CACHE:
        return CACHE[key][0]

    communicate = edge_tts.Communicate(text, VOICE)
    buf = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    mp3_bytes = buf.getvalue()
    CACHE[key] = (mp3_bytes, now)
    return mp3_bytes


class TTSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/speak":
            params = parse_qs(parsed.query)
            text = unquote(params.get("text", [""])[0])
            if not text:
                self.send_error(400, "Missing ?text=")
                return

            try:
                mp3 = asyncio.run(generate_audio(text))
            except Exception as e:
                self.send_error(500, str(e))
                return

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(mp3)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(mp3)
        elif parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f"OK — {VOICE} — {len(CACHE)} cached".encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def log_message(self, format, *args):
        # Quiet logging
        pass


def main():
    server = HTTPServer(("127.0.0.1", PORT), TTSHandler)
    print(f"🎙️  Questionarium TTS server running on http://localhost:{PORT}")
    print(f"   Voice: {VOICE}")
    print(f"   Test:  http://localhost:{PORT}/speak?text=Hello+from+Andrew")
    print(f"   Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down")
        server.server_close()


if __name__ == "__main__":
    main()
