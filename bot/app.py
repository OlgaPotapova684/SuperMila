"""
Сборка Application с обработчиками.
Используется для run_polling (локально) и для webhook (Vercel).
"""
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from bot.handlers.payment import callback_payment
from bot.handlers.start import cmd_start
from bot.handlers.subscription import callback_check_subscription
from config.settings import BOT_TOKEN


def build_application() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(callback_check_subscription, pattern="^check_subscription$"))
    app.add_handler(CallbackQueryHandler(callback_payment, pattern="^pay_rf$|^pay_world$"))
    return app
