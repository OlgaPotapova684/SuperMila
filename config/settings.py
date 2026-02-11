"""
Все настройки бота загружаются из переменных окружения.
Создайте файл .env на основе .env.example и заполните значения.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем .env из корня проекта
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").lstrip("@")
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
CHANNEL_INVITE_LINK = os.getenv("CHANNEL_INVITE_LINK", "")

# Закрытый канал после оплаты
CLOSED_CHANNEL_LINK = os.getenv("CLOSED_CHANNEL_LINK", "")

# Фото эксперта: путь относительно assets/ или абсолютный; для Vercel можно задать URL
EXPERT_PHOTO_URL = os.getenv("EXPERT_PHOTO_URL", "").strip()
EXPERT_PHOTO_PATH = os.getenv("EXPERT_PHOTO_PATH", "expert_photo.jpg")
if not Path(EXPERT_PHOTO_PATH).is_absolute():
    EXPERT_PHOTO_FULL = BASE_DIR / "assets" / EXPERT_PHOTO_PATH
else:
    EXPERT_PHOTO_FULL = Path(EXPERT_PHOTO_PATH)

# Таймер: задержка между сообщениями (секунды). 120 = 2 минуты
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "120"))
# На Vercel (serverless) таймер не работает — поставь True, тогда оба сообщения уйдут сразу подряд
SEND_WITHOUT_DELAY = os.getenv("SEND_WITHOUT_DELAY", "True").lower() in ("true", "1", "yes")

# Оплата
PAYMENT_SIMULATION = os.getenv("PAYMENT_SIMULATION", "True").lower() in ("true", "1", "yes")
SELLAMUS_PAYMENT_LINK_RF = os.getenv("SELLAMUS_PAYMENT_LINK_RF", "")
SELLAMUS_PAYMENT_LINK_WORLD = os.getenv("SELLAMUS_PAYMENT_LINK_WORLD", "")


def validate_config() -> list[str]:
    """Проверка обязательных настроек. Возвращает список ошибок."""
    errors = []
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN не задан в .env")
    if not CHANNEL_USERNAME and not CHANNEL_ID:
        errors.append("Укажите CHANNEL_USERNAME или CHANNEL_ID")
    if not CHANNEL_INVITE_LINK:
        errors.append("CHANNEL_INVITE_LINK не задан")
    if not CLOSED_CHANNEL_LINK:
        errors.append("CLOSED_CHANNEL_LINK не задан")
    # Фото не блокирует запуск: при отсутствии бот отправит только текст
    if not EXPERT_PHOTO_FULL.exists():
        import logging
        logging.getLogger(__name__).warning(
            "Файл фото эксперта не найден: %s — при /start будет отправлен только текст",
            EXPERT_PHOTO_FULL,
        )
    return errors
