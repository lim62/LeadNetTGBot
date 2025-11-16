from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.requests import (insert_name,
                                   insert_age,
                                   insert_story,
                                   insert_design)

async def name_handler(
    msg: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    await insert_name(
        session=session,
        telegram_id=msg.from_user.id,
        name=text
    )
    await dialog_manager.next()

async def age_handler(
    msg: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    await insert_age(
        session=session,
        telegram_id=msg.from_user.id,
        age=text
    )
    await dialog_manager.next()

async def story_handler(
    msg: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    await insert_story(
        session=session,
        telegram_id=msg.from_user.id,
        story=text
    )
    await dialog_manager.next()

async def design_handler(
    msg: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    await insert_design(
        session=session,
        telegram_id=msg.from_user.id,
        design=text
    )
    await dialog_manager.next()

async def no_text(
    msg: Message,
    widget: MessageInput,
    dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await msg.answer(i18n.user.no.text())