from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

def get_start_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.support(), url='https://t.me/assistpers')],
            [InlineKeyboardButton(text=i18n.btn.pulse(), callback_data='pulse'), InlineKeyboardButton(text=i18n.btn.pro_reactor(), callback_data='pro_reactor')]
        ]
    )

def get_back_kbd(i18n: TranslatorRunner, callback_data: str, text: str = None) -> InlineKeyboardMarkup:
    text = text if text else i18n.btn.back()
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
        ]
    )

def get_pulse_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.pusk_prepare(), callback_data='how_works_pulse')],
            [InlineKeyboardButton(text=i18n.btn.constructor(), callback_data='constructor')],
            [InlineKeyboardButton(text=i18n.btn.start_pulse(), callback_data='start_pulse')],
            [InlineKeyboardButton(text=i18n.btn.tarifs(), callback_data='tarifs')],
            [InlineKeyboardButton(text=i18n.btn.profile(), callback_data='profile')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_start')]
        ]
    )

def get_workpulse_kbd(i18n: TranslatorRunner, up_text: str | None = None, down_text: str | None = None, back_text: str | None = None, up: str = '', down: str = '', back: str = '', have_up: bool = True, have_down: bool = True, have_back: bool = True) -> InlineKeyboardMarkup:
    kbd: list[list[InlineKeyboardButton]] = []
    up_text = up_text if up_text else i18n.btn.previous()
    down_text = down_text if down_text else i18n.btn.next()
    back_text = back_text if back_text else i18n.btn.back()
    back = back if back else 'back_pulse'
    if have_up:
        kbd.append([InlineKeyboardButton(text=up_text, callback_data=up)])
    if have_down:
        kbd.append([InlineKeyboardButton(text=down_text, callback_data=down)])
    if have_back:
        kbd.append([InlineKeyboardButton(text=back_text, callback_data=back)])
    return InlineKeyboardMarkup(inline_keyboard=kbd)

def give_chats_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.previous(), callback_data='test_zalp')],
            [InlineKeyboardButton(text=i18n.btn.upload(), callback_data='upload_chats')],
            [InlineKeyboardButton(text=i18n.btn.contin(), callback_data='start_zalp')]
        ]
    )

def get_offer_kdb(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.examples_offer(), callback_data='examples_offer')],
            [InlineKeyboardButton(text=i18n.btn.constructor(), callback_data='constructor')],
            [InlineKeyboardButton(text=i18n.btn.next(), callback_data='test_zalp')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse')]
        ]
    )

def get_zalp_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.show_offer(), callback_data='show_offer')],
            [InlineKeyboardButton(text=i18n.btn.zalp(), callback_data='starting')],
            [InlineKeyboardButton(text=i18n.btn.edit_zalp(), callback_data='back_give_chats')]
        ]
    )

def get_end_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.previous(), callback_data='try_stories')],
            [InlineKeyboardButton(text=i18n.btn.constructor(), callback_data='constructor')],
            [InlineKeyboardButton(text=i18n.btn.tarifs(), callback_data='tarifs')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse')]
        ]
    )

def get_tarif_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.pulse_testum(), callback_data='pulse_testum')],
            [InlineKeyboardButton(text=i18n.btn.pulse_base(), callback_data='pulse_base')],
            [InlineKeyboardButton(text=i18n.btn.pulse_pro(), callback_data='pulse_pro')],
            [InlineKeyboardButton(text=i18n.btn.pulse_ultra(), callback_data='pulse_ultra')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse')]
        ]
    )

def get_verif_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.standard(), callback_data='standard'), InlineKeyboardButton(text=i18n.btn.fastlane(), callback_data='fastlane')],
            [InlineKeyboardButton(text=i18n.btn.cancel(), callback_data='back_start')]
        ]
    )

def get_fastlane_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.delta(), callback_data='delta')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_verif')]
        ]
    )

def get_delta_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.yes(), callback_data='back_fastlane'), InlineKeyboardButton(text=i18n.btn.no(), callback_data='back_verif')]
        ]
    )

def get_standard_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.true_back(), callback_data='back_start'), InlineKeyboardButton(text=i18n.btn.go_standard(), callback_data='product')]
        ]
    )

def get_send_kbd(i18n: TranslatorRunner, send_data: str, back_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.send(), callback_data=send_data)],
            [InlineKeyboardButton(text=i18n.btn.cancel(), callback_data=back_data)]
        ]
    )

def get_success_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # [InlineKeyboardButton(text=i18n.btn.neurohub(), callback_data='neurohub')],
            [InlineKeyboardButton(text=i18n.btn.menu(), callback_data='back_start')]
        ]
    )

def get_time_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.hurry(), callback_data=i18n.btn.hurry())],
            [InlineKeyboardButton(text=i18n.btn.week(), callback_data=i18n.btn.week())],
            [InlineKeyboardButton(text=i18n.btn.month(), callback_data=i18n.btn.month())],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_economics')]
        ]
    )

def get_accepted_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.demon(), url='https://t.me/m/HitWB64JMmNk')],
            [InlineKeyboardButton(text=i18n.btn.menu(), callback_data='back_start')]
        ]
    )

def get_declined_kbd(i18n: TranslatorRunner, other_text: str, other_call: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=other_text, callback_data=other_call)],
            [InlineKeyboardButton(text=i18n.btn.menu(), callback_data='back_start')]
        ]
    )