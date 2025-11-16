import asyncio

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InputMedia
from aiogram.exceptions import TelegramRetryAfter
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import AdminMainSG
from bot.database.requests import select_user, select_admin, update_user, insert_text, insert_photo

async def mailing_text_handler(
    msg: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    await insert_text(
        session=session,
        telegram_id=msg.from_user.id,
        mailing_text=msg.html_text
    )
    await dialog_manager.switch_to(AdminMainSG.mailing_photo)

async def mailing_photo_handler(
    media: InputMedia,
    widget: MessageInput,
    dialog_manager: DialogManager
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    model: dict = media.model_dump()
    await insert_photo(
        session=session,
        telegram_id=model['chat']['id'],
        photo=model['photo'][0]['file_id']
    )
    await dialog_manager.switch_to(AdminMainSG.sure_to_mail)

async def progress_mailing(
    call: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    bot: Bot = dialog_manager.middleware_data.get('bot')
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    users: list = await select_user(session=session)
    admin_text: list = [element for element in await select_admin(session=session)]
    if users:
        user_ids: list[int] = []
        for user in users:
            user_ids.append(user.telegram_id)
        for user_id in user_ids:
            try:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=admin_text[0].photo,
                    caption=admin_text[0].mailing_text
                )
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                pass
            finally:
                await asyncio.sleep(0.05)
        

async def delete_handler(
    call: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    result = await select_user(session)
    for user in result:
        await update_user(session, user.telegram_id)