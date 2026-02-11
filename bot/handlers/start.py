"""
Обработчик команды /start: фото эксперта + приветствие + кнопки.
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import welcome_keyboard
from bot.messages import WELCOME
from config.settings import CHANNEL_INVITE_LINK, EXPERT_PHOTO_FULL, EXPERT_PHOTO_URL


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_chat:
        return
    chat_id = update.effective_chat.id
    welcome_text = WELCOME.format(channel_link=CHANNEL_INVITE_LINK)
    keyboard = welcome_keyboard(CHANNEL_INVITE_LINK)

    if EXPERT_PHOTO_URL:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=EXPERT_PHOTO_URL,
            caption=welcome_text,
            reply_markup=keyboard,
            parse_mode=None,
        )
    elif EXPERT_PHOTO_FULL.exists():
        with open(EXPERT_PHOTO_FULL, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=welcome_text,
                reply_markup=keyboard,
                parse_mode=None,
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=keyboard,
        )
