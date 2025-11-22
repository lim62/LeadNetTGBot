import asyncio

from aiogram import Bot
from aiogram.types import Message

async def process_users_mailing(bot: Bot, msg: Message, ides: list[int]) -> None:
    for user_id in ides:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=msg.from_user.id,
                message_id=msg.message_id
            )
        except Exception:
            pass
        finally:
            await asyncio.sleep(0.5)