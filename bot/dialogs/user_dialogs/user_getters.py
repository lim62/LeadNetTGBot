from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

async def name_getter(dialog_manager: DialogManager, **kwargs) -> dict[str: str]:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.user.name()
    }

async def age_getter(dialog_manager: DialogManager, **kwargs) -> dict[str: str]:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.user.age()
    }

async def story_getter(dialog_manager: DialogManager, **kwargs) -> dict[str: str]:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.user.story()
    }

async def design_getter(dialog_manager: DialogManager, **kwargs) -> dict[str: str]:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.user.design()
    }

async def final_getter(dialog_manager: DialogManager, **kwargs) -> dict[str: str]:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    return {
        'text': i18n.user.final(),
        'button_text': i18n.button.blog()
    }