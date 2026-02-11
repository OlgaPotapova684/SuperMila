"""
Vercel serverless: приём webhook от Telegram.
Telegram шлёт сюда POST с обновлениями; обрабатываем и отвечаем 200.
"""
import asyncio
import json
import logging
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Корень проекта в path, чтобы находились bot и config (на Vercel cwd может быть api/)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from telegram import Update
from bot.app import build_application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_response(400)
            self.end_headers()
            return
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode("utf-8"))
        except Exception as e:
            logger.warning("Invalid JSON: %s", e)
            self.send_response(400)
            self.end_headers()
            return
        app = build_application()
        update = Update.de_json(data, app.bot)
        if update is None:
            self.send_response(200)
            self.end_headers()
            return
        async def run():
            await app.initialize()
            await app.start()
            try:
                await app.process_update(update)
            finally:
                await app.shutdown()
        try:
            asyncio.run(run())
        except Exception as e:
            logger.exception("Error processing update: %s", e)
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))
