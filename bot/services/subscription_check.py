"""
Проверка подписки пользователя на канал.
"""
from telegram import Bot
from telegram.constants import ChatMemberStatus


async def is_user_subscribed(bot: Bot, channel_id: str, user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на канал.
    channel_id: числовой ID канала (например -1001234567890) или @username.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        status = member.status
        return status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        )
    except Exception:
        return False
