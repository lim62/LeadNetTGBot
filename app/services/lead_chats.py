import asyncio

from asyncio.exceptions import CancelledError
from typing import TYPE_CHECKING
from pyrogram import Client
from pyrogram.types import Message
from bot.logs.logs import print_info, print_warn, print_error

if (TYPE_CHECKING):
    from app.qt_windows.bot_window import BotWindow

async def send_callback(self: 'BotWindow', client: Client, message: any, text: str, BOT: str) -> None:
    if message.reply_markup:
        for row in message.reply_markup.inline_keyboard:
            for button in row:
                if text in button.text.lower():
                    await client.request_callback_answer(
                        chat_id=BOT,
                        message_id=message.id,
                        callback_data=button.callback_data
                    )

async def get_last_message(client: Client, BOT: str) -> any:
    async for msg in client.get_chat_history(BOT, limit=2):
        if msg:
            return msg
        
async def collecting_data(message: Message, to_add: list[str]) -> int:
    text: list[str] = message.text.split('@')[2:]
    lines: list[str] = []
    for line in text:
        lines.append(line.split(' '))
    for line in lines:
        link = f'https://t.me/{line[0]}'
        if link not in to_add:
            to_add.append(link)
            with open(('bot/database/leads_chats.txt'), 'a') as file:
                file.write(f'\n{link}')
    text: list[str] = message.text.split('страница')[-1]
    return int(text.split(' ')[-1])

async def process_lead_chats(self: 'BotWindow', contacts: list[str]) -> None:
    print_info('Начал сбор чатов...')
    BOT: str = 'LNStat_Bot'
    leads_chats: list[str] = []
    used_contacts: list[str] = []
    message: None = None
    counter: int = 0
    tried_pages: int = 0
    with open(('bot/database/leads_chats.txt'), 'r') as file:
        leads_chats = [link.strip() for link in file.readlines() if link.startswith('http')]
    with open(('bot/database/used_contacts.txt'), 'r') as file:
        used_contacts = [contact.strip() for contact in file.readlines() if contact.startswith('@')]
    while True:
        if self.clients:
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
    for client in self.clients:
        try:
            await client.join_chat("datais")
        except Exception:
            pass
    try:
        for contact in contacts:
            if contact not in used_contacts:
                self._was_lead[client.name] += 1
                tried_pages = 1
                used_contacts.append(contact)
                with open(('bot/database/used_contacts.txt'), 'a') as file:
                    file.write(f'\n{contact}')
                with open(('bot/database/leads_chats.txt'), 'a') as file:
                    file.write('\n')
                counter += 1
                client = self.get_next_client(self.clients)
                print_info(client.name)
                await asyncio.sleep(1)
                try:
                    await client.send_message(BOT, '/start')
                    await asyncio.sleep(1)
                    await client.send_message(BOT, contact)
                    await asyncio.sleep(1)
                    message = await get_last_message(client, BOT)
                    await send_callback(self, client, message, "чаты", BOT)
                    await asyncio.sleep(1)
                    message = await get_last_message(client, BOT)
                    pages = await collecting_data(message=message, to_add=leads_chats)
                    while tried_pages < pages:
                        tried_pages += 1
                        await send_callback(self, client, message, "→", BOT)
                        await asyncio.sleep(1)
                        message = await get_last_message(client, BOT)
                        await collecting_data(message=message, to_add=leads_chats)
                except Exception as e:
                    raise e()
                else:
                    print_info(f'Контакт #{counter} {contact} собран')
            else:
                print_info(f'Контакт {contact} уже собран')
        print_info('Сборка закончена')
        self.update_error('green', f'Собрал {counter} людей')
        self.lead_path.setText('')
    except CancelledError:
        print_info('Команда отменена')
    except Exception as e:
        self.update_error('red', 'Ошибка (посмотри консоль)')
        print_error(f'Ошибка сбора {e}')
    self.stop.hide()
    self.chats.show()
    self.enable_items(True)
        