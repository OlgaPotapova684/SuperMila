"""
Обработка нажатия «Я уже подписан/а»: каскад из двух сообщений с паузой DELAY_SECONDS.
Проверка подписки отключена — каскад отправляется всегда при нажатии кнопки.
"""
import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import payment_keyboard
from bot.messages import (
    AFTER_SUBSCRIPTION,
    DELAYED_MESSAGE,
    SUBSCRIBED_CONFIRM,
    VIDEO_TRAINING_TITLE,
)
from config.settings import (
    DELAY_SECONDS,
    PAYMENT_SIMULATION,
    SELLAMUS_PAYMENT_LINK_RF,
    SELLAMUS_PAYMENT_LINK_WORLD,
)

logger = logging.getLogger(__name__)


async def callback_check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатия «Я уже подписан/а» — всегда отправляем каскад из двух сообщений."""
    query = update.callback_query
    if not query or not query.message or not update.effective_user:
        return
    await query.answer()

    chat_id = query.message.chat_id

    # Короткое подтверждение, через DELAY_SECONDS первое сообщение, ещё через DELAY_SECONDS второе
    try:
        await context.bot.send_message(chat_id=chat_id, text=SUBSCRIBED_CONFIRM)
    except Exception as e:
        logger.exception("Failed to send SUBSCRIBED_CONFIRM: %s", e)
    await asyncio.sleep(DELAY_SECONDS)
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{VIDEO_TRAINING_TITLE}\n\n{AFTER_SUBSCRIPTION}",
        )
    except Exception as e:
        logger.exception("Failed to send first message: %s", e)
    await asyncio.sleep(DELAY_SECONDS)
    try:
        keyboard = payment_keyboard(
            SELLAMUS_PAYMENT_LINK_RF,
            SELLAMUS_PAYMENT_LINK_WORLD,
            PAYMENT_SIMULATION,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=DELAYED_MESSAGE,
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.exception("Failed to send second message: %s", e)
