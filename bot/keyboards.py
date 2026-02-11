"""
Клавиатуры бота (inline-кнопки).
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def welcome_keyboard(channel_invite_link: str) -> InlineKeyboardMarkup:
    """Кнопки после приветствия: проверка подписки и подписаться."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Я уже подписан/а", callback_data="check_subscription")],
        [InlineKeyboardButton("Подписаться на канал", url=channel_invite_link)],
    ])


def payment_keyboard(
    payment_link_rf: str | None,
    payment_link_world: str | None,
    simulation: bool,
) -> InlineKeyboardMarkup:
    """
    Кнопки оплаты.
    Если simulation=True и ссылок нет — показываем кнопки имитации.
    Иначе — ссылки на Продамус.
    """
    if simulation and not payment_link_rf and not payment_link_world:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("По картам РФ (имитация)", callback_data="pay_rf")],
            [InlineKeyboardButton("С любой точки мира (имитация)", callback_data="pay_world")],
        ])
    rows = []
    if payment_link_rf:
        rows.append([InlineKeyboardButton("По картам РФ", url=payment_link_rf)])
    if payment_link_world:
        rows.append([InlineKeyboardButton("С любой точки мира", url=payment_link_world)])
    if not rows:
        rows = [
            [InlineKeyboardButton("По картам РФ (имитация)", callback_data="pay_rf")],
            [InlineKeyboardButton("С любой точки мира (имитация)", callback_data="pay_world")],
        ]
    return InlineKeyboardMarkup(rows)
