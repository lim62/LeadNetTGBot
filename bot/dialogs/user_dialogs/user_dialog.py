from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.media import StaticMedia
from bot.states import UserMainSG
from bot.dialogs.user_dialogs.user_getters import (name_getter,
                                                   age_getter,
                                                   story_getter,
                                                   design_getter,
                                                   final_getter)
from bot.dialogs.user_dialogs.user_handlers import (name_handler,
                                                    age_handler,
                                                    story_handler,
                                                    design_handler,
                                                    no_text)

user_main_dialog = Dialog(
    Window(
        Format('{text}'),
        TextInput(
            id='name_input',
            on_success=name_handler
        ),
        MessageInput(
            func=no_text
        ),
        state=UserMainSG.name,
        getter=name_getter
    ),
    Window(
        Format('{text}'),
        TextInput(
            id='age_input',
            on_success=age_handler
        ),
        MessageInput(
            func=no_text
        ),
        state=UserMainSG.age,
        getter=age_getter
    ),
    Window(
        Format('{text}'),
        TextInput(
            id='story_input',
            on_success=story_handler
        ),
        MessageInput(
            func=no_text
        ),
        state=UserMainSG.story,
        getter=story_getter
    ),
    Window(
        StaticMedia(
            path='bot/media/story_photo.jpg'
        ),
        Format('{text}'),
        TextInput(
            id='design_input',
            on_success=design_handler
        ),
        MessageInput(
            func=no_text
        ),
        state=UserMainSG.design,
        getter=design_getter
    ),
    Window(
        Format('{text}'),
        Url(
            text=Format('{button_text}'),
            url=Const('https://t.me/avirovees/581')
        ),
        state=UserMainSG.final,
        getter=final_getter
    )
)