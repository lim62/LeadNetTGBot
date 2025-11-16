from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.input import MessageInput, TextInput
from bot.states import AdminMainSG
from bot.dialogs.admin_dialogs.admin_handlers import (mailing_text_handler,
                                                      mailing_photo_handler,
                                                      progress_mailing,
                                                      delete_handler)
from bot.dialogs.admin_dialogs.admin_getters import (menu_getter,
                                                     contacts_getter,
                                                     database_getter,
                                                     mailing_text_getter,
                                                     mailing_photo_getter,
                                                     clean_contacts_getter,
                                                     sure_to_mail_getter)

admin_main_dialog = Dialog(
    Window(
        Format('{text}'),
        Row(
            SwitchTo(text=Format('{contacts_text}'), id='change_contacts', state=AdminMainSG.contacts),
            SwitchTo(text=Format('{database_text}'), id='change_database', state=AdminMainSG.database)
        ),
        Row(
            SwitchTo(text=Format('{mailing_text}'), id='change_mailing', state=AdminMainSG.mailing_text)
        ),
        getter=menu_getter,
        state=AdminMainSG.menu
    ),
    Window(
        Format('{text}'),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_contacts', state=AdminMainSG.menu),
            SwitchTo(text=Format('{delete_text}'), id='delete_contacts', state=AdminMainSG.clean_contacts, when='should_delete')
        ),
        getter=contacts_getter,
        state=AdminMainSG.contacts
    ),
    Window(
        Format('{text}'),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_database', state=AdminMainSG.menu),
        ),
        getter=database_getter,
        state=AdminMainSG.database
    ),
    Window(
        Format('{text}'),
        TextInput(
            id='mailing_text',
            on_success=mailing_text_handler
        ),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_mailing', state=AdminMainSG.menu)
        ),
        getter=mailing_text_getter,
        state=AdminMainSG.mailing_text
    ),
    Window(
        Format('{text}'),
        MessageInput(
            content_types=ContentType.PHOTO,
            func=mailing_photo_handler
        ),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_mailing', state=AdminMainSG.menu)
        ),
        getter=mailing_photo_getter,
        state=AdminMainSG.mailing_photo
    ),
    Window(
        Format('{text}'),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_delete_contacts', state=AdminMainSG.menu),
            SwitchTo(text=Format('{progress_text}'), id='progress_delete_contacts', state=AdminMainSG.menu, on_click=delete_handler)
        ),
        getter=clean_contacts_getter,
        state=AdminMainSG.clean_contacts
    ),
    Window(
        Format('{text}'),
        Row(
            SwitchTo(text=Format('{cancel_text}'), id='cancel_doing_mailing', state=AdminMainSG.menu),
            SwitchTo(text=Format('{progress_text}'), id='progress_mailing', state=AdminMainSG.menu, on_click=progress_mailing)
        ),
        getter=sure_to_mail_getter,
        state=AdminMainSG.sure_to_mail
    )
)