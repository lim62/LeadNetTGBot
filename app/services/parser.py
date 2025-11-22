import asyncio

from asyncio.exceptions import CancelledError
from typing import TYPE_CHECKING
from pyrogram import Client
from bot.logs import print_info, print_warn, print_error

if (TYPE_CHECKING):
    from app.qt_windows.bot_window import BotWindow

async def proccess_async_parser(self: 'BotWindow', link: str) -> None:
    print_info('Парсер начал работу')
    counter: int = 0
    alert_msg: int = 0
    usernames: list = []
    already_in: list = []
    while True:
        if self.clients:
            client: Client = self.clients[0]
            self.update_error('green', 'Выполняю...')
            alert_msg = 0
            break
        else:
            if alert_msg == 0:
                print_warn('Жду активные аккаунты')
                self.update_error('#FFA200', 'Жду активные аккаунты')
                alert_msg += 1
            await asyncio.sleep(1)
            continue
    try:
        if link.startswith('https://t.me/+') or link.startswith('http://t.me/+') or link.startswith('https://t.me/joinchat') or link.startswith('http://t.me/joinchat'):
            link = link
        elif link.startswith('https://t.me/') or link.startswith('http://t.me/'):
            dashes: int = link.count('/')
            link = link.split('/')[-1 - (dashes - 3)]
        try:
            chat = await client.join_chat(link)
        except Exception:
            chat = await client.get_chat(link)
        print_info('Парсер присоеденился к чату')
        await asyncio.sleep(1)
        async for msg in client.get_chat_history(chat.id, limit=5000):
            if msg:
                if msg.from_user:
                    if msg.from_user.username:
                        usernames.append(msg.from_user.username)
        with open(('bot/database/contacts.txt'), 'r') as file:
            already_in = [username.strip() for username in file.readlines() if username]
        with open(('bot/database/contacts.txt'), 'a') as file:
            for username in set(usernames):
                if f'@{username}' not in already_in:
                    counter += 1
                    file.write(f'\n@{username}')
        print_info('Парсер успешно закончил работу')
        self.update_error('green', f'+{counter} контактов')
        self.parse_link.setText('')
    except CancelledError:
        print_info('Команда отменена')
    except Exception as e:
        self.update_error('red', 'Ошибка (посмотри консоль)')
        print_error(f'Ошибка парсера {e}')
    self.stop.hide()
    self.chats.show()
    self.enable_items(True)