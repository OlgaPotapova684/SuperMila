"""
Проверка подписки и выдача контента после проверки.
Запуск отложенного сообщения (через DELAY_SECONDS).
"""
import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import payment_keyboard, welcome_keyboard
from bot.messages import (
    AFTER_SUBSCRIPTION,
    DELAYED_MESSAGE,
    NOT_SUBSCRIBED,
    VIDEO_TRAINING_TITLE,
)
from bot.services.subscription_check import is_user_subscribed
from config.settings import (
    CHANNEL_ID,
    CHANNEL_INVITE_LINK,
    CHANNEL_USERNAME,
    DELAY_SECONDS,
    PAYMENT_SIMULATION,
    SELLAMUS_PAYMENT_LINK_RF,
    SELLAMUS_PAYMENT_LINK_WORLD,
)


async def _send_delayed_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    """Отправка второго сообщения по таймеру с кнопками оплаты."""
    await asyncio.sleep(DELAY_SECONDS)
    keyboard = payment_keyboard(
        SELLAMUS_PAYMENT_LINK_RF,
        SELLAMUS_PAYMENT_LINK_WORLD,
        PAYMENT_SIMULATION,
    )
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=DELAYED_MESSAGE,
            reply_markup=keyboard,
        )
    except Exception:
        pass


async def callback_check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатия «Я уже подписан/а»."""
    query = update.callback_query
    if not query or not query.message or not update.effective_user:
        return
    await query.answer()

    user_id = update.effective_user.id
    chat_id = query.message.chat_id
    channel_id = CHANNEL_ID or f"@{CHANNEL_USERNAME}"

    subscribed = await is_user_subscribed(context.bot, channel_id, user_id)

    if not subscribed:
        await context.bot.send_message(
            chat_id=chat_id,
            text=NOT_SUBSCRIBED,
            reply_markup=welcome_keyboard(CHANNEL_INVITE_LINK),
        )
        return

    # Подписан — отправляем блок «Видео-тренировка» и текст подарков
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"<b>{VIDEO_TRAINING_TITLE}</b>\n\n{AFTER_SUBSCRIPTION}",
        parse_mode="HTML",
    )

    # Запускаем таймер на второе сообщение (про 490р и оплату)
    asyncio.create_task(_send_delayed_message(context, chat_id))
