from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

def get_start_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.pulse(), callback_data='pulse'), InlineKeyboardButton(text=i18n.btn.pulse(), callback_data='pulse1')],
            [InlineKeyboardButton(text=i18n.btn.verification(), callback_data='verification'), InlineKeyboardButton(text=i18n.btn.neurohub(), callback_data='neurohub')],
            [InlineKeyboardButton(text=i18n.btn.pro_reactor(), callback_data='pro_reactor'), InlineKeyboardButton(text=i18n.btn.traffic(), callback_data='traffic')],
            [InlineKeyboardButton(text=i18n.btn.support(), url='https://t.me')]
        ]
    )

def get_back_kbd(i18n: TranslatorRunner, callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data=callback_data)]
        ]
    )

def get_pulse_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.what_pulse(), callback_data='what_pulse')],
            [InlineKeyboardButton(text=i18n.btn.work_pulse(), callback_data='work_pulse')],
            [InlineKeyboardButton(text=i18n.btn.tarifs(), callback_data='tarifs')],
            [InlineKeyboardButton(text=i18n.btn.constructor(), callback_data='constructor')],
            [InlineKeyboardButton(text=i18n.btn.start_pulse(), callback_data='start_pulse')],
            [InlineKeyboardButton(text=i18n.btn.my_campaings(), callback_data='campaings')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_start')]
        ]
    )

def get_pulse_kbd1(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.pusk_prepare(), callback_data='pusk_prepare')],
            [InlineKeyboardButton(text=i18n.btn.what_pulse(), callback_data='what_pulse1')],
            [InlineKeyboardButton(text=i18n.btn.constructor(), callback_data='constructor1')],
            [InlineKeyboardButton(text=i18n.btn.start_pulse(), callback_data='what_stage33')],
            [InlineKeyboardButton(text=i18n.btn.tarifs(), callback_data='tarifs')],
            [InlineKeyboardButton(text=i18n.btn.my_campaings(), callback_data='campaings1')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_start')]
        ]
    )

def get_workpulse_kbd(i18n: TranslatorRunner, up_text: str | None = None, down_text: str | None = None, up: str = '', down: str = '', have_up: bool = True, have_down: bool = True) -> InlineKeyboardMarkup:
    kbd: list[list] = []
    up_text = up_text if up_text else i18n.btn.previous()
    down_text = down_text if down_text else i18n.btn.next()
    if have_up:
        kbd.append([InlineKeyboardButton(text=up_text, callback_data=up)])
    if have_down:
        kbd.append([InlineKeyboardButton(text=down_text, callback_data=down)])
    kbd.append([InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse1')])
    return InlineKeyboardMarkup(
        inline_keyboard=kbd
    )

def get_totarif_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔺', callback_data='how_stage8')],
            [InlineKeyboardButton(text=i18n.btn.tarifs(), callback_data='tarifs')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse')]
        ]
    )

def get_tarif_kbd(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.btn.pulse_threedays(), callback_data='pulse_threedays')],
            [InlineKeyboardButton(text=i18n.btn.pulse_tendays(), callback_data='pulse_tendays')],
            [InlineKeyboardButton(text=i18n.btn.pulse_month(), callback_data='pulse_month')],
            [InlineKeyboardButton(text=i18n.btn.back(), callback_data='back_pulse1')]
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
            [InlineKeyboardButton(text=i18n.btn.cancel(), callback_data='back_verif'), InlineKeyboardButton(text=i18n.btn.go_standard(), callback_data='product')]
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
            [InlineKeyboardButton(text=i18n.btn.neurohub(), callback_data='neurohub')],
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