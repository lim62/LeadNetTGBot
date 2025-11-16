from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import AdminMainSG
from bot.database.requests import insert_admin

admin_router = Router()

@admin_router.message(CommandStart())
async def admin_cmd_start(msg: Message, dialog_manager: DialogManager, session: AsyncSession) -> None:
    """await insert_admin(
        session=session,
        telegram_id=msg.from_user.id,
        mailing_text=None,
        photo=None
    )"""
    await dialog_manager.start(AdminMainSG.menu, mode=StartMode.RESET_STACK)
