import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from app.settings import start_clients
from bot.config import Config, load_config
from bot.handlers import admin_router, user_router
from bot.filters import AdminFilter
from bot.storage import load_storage, get_rstorage
from bot.middlewares import DataMiddleware
from bot.utils import create_translator_hub
from bot.database import Base

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
    engine: AsyncEngine = create_async_engine(
        url=str(config.database.DSN),
        echo=config.database.is_echo
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    rstorage = get_rstorage(config)
    dp = Dispatcher(storage=await load_storage(config), _translator_hub=translator_hub)
    dp.include_routers(admin_router, user_router)
    dp.update.middleware(DataMiddleware(rstorage=rstorage, bot=bot, config=config, session_maker=session_maker))
    admin_router.message.filter(AdminFilter(config))
    admin_router.callback_query.filter(AdminFilter(config))
    await start_clients(session_maker=session_maker, rstorage=rstorage)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())