from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.requests import select_user

async def menu_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.admin.menu(),
        'contacts_text': i18n.button.contacts(),
        'database_text': i18n.button.database(),
        'mailing_text': i18n.button.mailing()
    }

async def contacts_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    text: str = ''
    should_delete: bool = True
    result = await select_user(session)
    if result:
        text = i18n.admin.contacts()
        for user in result:
            if user.design:
                text += '\n\n'
                text += i18n.admin.load.contact(
                    username=user.username,
                    name=user.name,
                    age=user.age,
                    story=user.story,
                    design=user.design
                )
        if text == i18n.admin.contacts():
            should_delete = False
            text = i18n.admin.no.contacts()
    else:
        should_delete = False
        text = i18n.admin.no.contacts()
    return {
        'text': text,
        'should_delete': should_delete,
        'delete_text': i18n.button.clear(),
        'cancel_text': i18n.button.cancel()
    }

async def database_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    text: str
    result = await select_user(session)
    if result:
        text = i18n.admin.database()
        for user in result:
            text += '\n\n'
            text += user.username
    else: 
        text = i18n.admin.no.database()
    return {
        'text': text,
        'cancel_text': i18n.button.cancel()
    }

async def mailing_text_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.admin.mailing.text(),
        'cancel_text': i18n.button.cancel()
    }

async def mailing_photo_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.admin.mailing.photo(),
        'cancel_text': i18n.button.cancel()
    }

async def clean_contacts_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.admin.clean.contacts(),
        'cancel_text': i18n.button.no(),
        'progress_text': i18n.button.yes()
    }

async def sure_to_mail_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.admin.sure.to.mail(),
        'cancel_text': i18n.button.no(),
        'progress_text': i18n.button.yes()
    }