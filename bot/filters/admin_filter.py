from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from bot.config import Config

class AdminFilter(BaseFilter):
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        return True if obj.from_user.id in self.config.bot.ADMINS_IDS else False