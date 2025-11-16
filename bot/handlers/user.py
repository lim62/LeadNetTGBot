from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import UserMainSG
from bot.database.requests import insert_user

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(msg: Message, dialog_manager: DialogManager, session: AsyncSession) -> None:
    """await insert_user(
        session=session,
        telegram_id=msg.from_user.id,
        username=f'@{msg.from_user.username}',
        name=None,
        age=None,
        story=None,
        design=None
    )"""
    await dialog_manager.start(UserMainSG.name, mode=StartMode.RESET_STACK)