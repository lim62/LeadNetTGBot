from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class SessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker, bot: Bot) -> None:
        super().__init__()
        self.session_pool = session_pool
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        data['bot'] = self.bot
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)       