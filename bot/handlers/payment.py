"""
Обработка нажатий на кнопки оплаты.
В режиме имитации: сразу отправляем ссылку на закрытый канал.
В реальном режиме: можно отправить ссылку на оплату или ждать webhook от Продамус.
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import AFTER_PAYMENT
from config.settings import CLOSED_CHANNEL_LINK, PAYMENT_SIMULATION


async def callback_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатия «По картам РФ» или «С любой точки мира» (callback при имитации)."""
    query = update.callback_query
    if not query or not query.message or not update.effective_chat:
        return

    await query.answer("Оплата прошла (имитация). Ссылка на канал — в сообщении ниже.")

    if PAYMENT_SIMULATION:
        text = AFTER_PAYMENT.format(closed_channel_link=CLOSED_CHANNEL_LINK)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )
    # else: реальная оплата — ссылки ведут на Продамус, после оплаты webhook отправит ссылку
    # или пользователь нажимает "Я оплатил" и мы проверяем через API Продамус
