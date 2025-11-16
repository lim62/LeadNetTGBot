from fluentogram import TranslatorHub, FluentTranslator
from fluentogram.translator import FluentBundle

def create_translator_hub() -> TranslatorHub:
    return TranslatorHub(
        locales_map={
            'ru': ('ru', 'en'),
            'en': ('en', 'ru')
        },
        translators=[
            FluentTranslator(
                locale='ru',
                translator=FluentBundle.from_files(
                    locale='ru-RU',
                    filenames=['bot/locales/ru/LC_MESSAGES/txt.ftl']
                )
            ),
            FluentTranslator(
                locale='en',
                translator=FluentBundle.from_files(
                    locale='en-US',
                    filenames=['bot/locales/ru/LC_MESSAGES/txt.ftl']
                )
            )
        ]
    )