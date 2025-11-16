import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from fluentogram import TranslatorHub
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from bot.config import Config, load_config
from bot.handlers import admin_router, user_router
from bot.dialogs import admin_main_dialog, user_main_dialog
from bot.filters import AdminFilter
from bot.database import Base
from bot.storage import load_storage
from bot.middlewares import TranslatorRunnerMiddleware, SessionMiddleware
from bot.utils import create_translator_hub

async def main() -> None:
    config: Config = load_config()
    translator_hub: TranslatorHub = create_translator_hub()
    bot = Bot(
        token=config.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    logging.basicConfig(
        level=config.log.LEVEL,
        format=config.log.FORMAT,
        style='{'
    )
    """engine: AsyncEngine = create_async_engine(
        url=str(config.database.DSN),
        echo=False
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    session: AsyncSession = async_sessionmaker(engine, expire_on_commit=False)"""
    dp = Dispatcher(storage=await load_storage(config), _translator_hub=translator_hub)
    dp.include_routers(admin_router, user_router)
    dp.include_routers(admin_main_dialog, user_main_dialog)
    setup_dialogs(dp)
    #dp.update.middleware(SessionMiddleware(session, bot))
    dp.update.middleware(TranslatorRunnerMiddleware())
    admin_router.message.filter(AdminFilter(config))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())