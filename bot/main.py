"""
Точка входа для локального запуска (long polling).
На Vercel используется webhook: api/telegram_webhook.py
"""
import logging

from bot.app import build_application
from config.settings import validate_config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    errors = validate_config()
    if errors:
        for e in errors:
            logger.error(e)
        raise SystemExit("Исправьте конфигурацию в .env (см. .env.example)")

    app = build_application()
    logger.info("Бот запущен (polling)")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
