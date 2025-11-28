from redis import Redis
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

def get_leadpanel_kbd(i18n: TranslatorRunner, meta: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.decline(), callback_data=f'decline_{meta}'), InlineKeyboardButton(text=i18n.btn.call(), callback_data=f'call_{meta}')],
            [InlineKeyboardButton(text=i18n.btn.watcher(), callback_data=f'watcher_{meta}')]
        ]
    )

def get_yes_no_kbd(i18n: TranslatorRunner, on_yes: str, on_no: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.yes(), callback_data=on_yes), InlineKeyboardButton(text=i18n.btn.cancel(), callback_data=on_no)]
        ]
    )

def get_startpanel_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.admin.accounts(), callback_data='accounts')],
            [InlineKeyboardButton(text=i18n.btn.admin.mailing(), callback_data='mailing'), InlineKeyboardButton(text=i18n.btn.admin.to_menu(), callback_data='back_start')],
            [InlineKeyboardButton(text=i18n.btn.admin.database(), callback_data='database'), InlineKeyboardButton(text=i18n.btn.admin.status(), callback_data='change_status')],
            [InlineKeyboardButton(text=i18n.btn.soft(), callback_data='soft')]
        ]
    )

async def get_accounts_kbd(i18n: TranslatorRunner, clients: list, rstorage: Redis) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    for client in clients:
        phone = client.phone_number
        is_active = int(await rstorage.get(phone))
        new_phone = f'💥 {phone}' if is_active == 1 else phone
        keyboard.append([InlineKeyboardButton(text=new_phone, callback_data=phone)])
    keyboard.append([InlineKeyboardButton(text=i18n.btn.add_accs(), callback_data='add_accs'), InlineKeyboardButton(text=i18n.btn.delete_accs(), callback_data='delete_accs')])
    keyboard.append([InlineKeyboardButton(text=i18n.btn.recieve_code(), callback_data='receive_code')])
    keyboard.append([InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_admin_menu')])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def get_change_status_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.status_user(), callback_data='status_user')],
            [InlineKeyboardButton(text=i18n.btn.status_paid(), callback_data='status_paid')],
            [InlineKeyboardButton(text=i18n.btn.true_back(), callback_data='change_status')]
        ]
    )

def get_soft_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.parsing(), callback_data='parsing')],
            [InlineKeyboardButton(text=i18n.btn.inviting(), callback_data='inviting')],
            [InlineKeyboardButton(text=i18n.btn.groups(), callback_data='groups')],
            [InlineKeyboardButton(text=i18n.btn.private(), callback_data='private')],
            [InlineKeyboardButton(text=i18n.btn.leads(), callback_data='leads')],
            [InlineKeyboardButton(text=i18n.btn.dustsos(), callback_data='dustsos')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_admin_menu')]
        ]
    )