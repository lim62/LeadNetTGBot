from typing import Any, Callable, Awaitable
from pyrogram import Client
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from aiogram.fsm.storage.redis import RedisStorage
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from bot.config import Config

class DataMiddleware(BaseMiddleware):
    def __init__(self, config: Config, bot: Bot, clients: list[Client], rstorage: RedisStorage, session_maker: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.config = config
        self.bot = bot
        self.rstorage = rstorage
        self.session_maker = session_maker
        self.clients = clients
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        translator_hub: TranslatorHub = data.get('_translator_hub')
        data['i18n'] = translator_hub.get_translator_by_locale(locale='ru')
        data['config'] = self.config
        data['bot'] = self.bot
        data['clients'] = self.clients
        data['rstorage'] = self.rstorage
        data['session_maker'] = self.session_maker
        return await handler(event, data)       