import asyncio

from redis import Redis
from fluentogram import TranslatorRunner
from aiogram.types import Message, FSInputFile
from asyncio.exceptions import CancelledError
from pyrogram import Client
from app.logs import print_info, print_error

async def proccess_async_parser(clients: Client, i18n: TranslatorRunner, rstorage: Redis, msg: Message, links: list[str]) -> None:
    counter: int = 0
    print(len(clients))
    usernames: list = []
    with open(('bot/media/contacts.txt'), 'w') as file:
        file.write(' ')
    try:
        for link in links:
            counter += 1
            client: Client = clients[counter % len(clients)]
            await print_info(msg, f'Работаю с {link}')
            await asyncio.sleep(1)
            if link.startswith('https://t.me/+') or link.startswith('http://t.me/+') or link.startswith('https://t.me/joinchat') or link.startswith('http://t.me/joinchat'):
                link = link
            elif link.startswith('https://t.me/') or link.startswith('http://t.me/'):
                dashes: int = link.count('/')
                link = link.split('/')[-1 - (dashes - 3)]
            try:
                chat = await client.join_chat(link)
            except Exception:
                chat = await client.get_chat(link)
            await print_info(msg, 'Парсер присоеденился к чату')
            await asyncio.sleep(1)
            await print_info(msg, 'Парсер собирает контакты...')
            async for msg in client.get_chat_history(chat.id, limit=5000):
                if msg:
                    if msg.from_user:
                        if msg.from_user.username:
                            usernames.append(msg.from_user.username)
            with open(('bot/media/contacts.txt'), 'a') as file:
                for username in set(usernames):
                    file.write(f'\n@{username}')
            await msg.delete()
            await msg.answer_document(
                document=FSInputFile('bot/media/database.txt')
            )
    except CancelledError:
        await print_info(msg, 'Команда отменена')
    except Exception as e:
        await print_error(msg, f'Ошибка парсера {e}')