import asyncio

from random import randint
from math import ceil
from typing import TYPE_CHECKING
from asyncio.exceptions import CancelledError
from pyrogram import Client
from pyrogram.errors.exceptions import (ChatWriteForbidden, FloodWait,
                                        UsernameNotOccupied, PeerFlood,
                                        ChannelInvalid, UsersTooMuch,
                                        ChannelPrivate)
from bot.logs import print_info, print_error, print_warn
from bot.services.utils import account_waiting

if (TYPE_CHECKING):
    from app.qt_windows.bot_window import BotWindow

async def proccess_async_inviter(self: 'BotWindow', link: str, INVITE_DELAY: int) -> None:
    print_info('Инвайтер начал работу')
    counter: int = 0
    alert_msg: int = 0
    tried_accounts: int = 0
    contacts: list[str] = []
    invited_contacts: list[str] = []
    need_chat: bool = True
    try:
        with open(('bot/database/contacts.txt'), 'r') as file:
            contacts = [contact[1:].replace('\n', '') for contact in file.readlines() if contact != '\n']
        with open(('bot/database/invited_contacts.txt'), 'r') as file:
            invited_contacts = [invited_contact[1:].replace('\n', '') for invited_contact in file.readlines() if invited_contact != '\n']
        if link.startswith('https://t.me/+') or link.startswith('http://t.me/+') or link.startswith('https://t.me/joinchat') or link.startswith('http://t.me/joinchat'):
            link = link
        elif link.startswith('https://t.me/') or link.startswith('http://t.me/'):
            dashes: int = link.count('/')
            link = link.split('/')[-1 - (dashes - 3)]
        for contact in contacts:
            if contact not in invited_contacts:
                counter += 1
                alert_msg = 0
                while True:
                    if self.clients:
                        delay: int = INVITE_DELAY / len(self.clients)
                        for_sleep = randint(ceil(delay), ceil(delay) + 5)
                        client: Client = self.get_next_client(self.clients)
                        self.update_error('green', 'Выполняю...')
                        alert_msg = 0
                    else:
                        if alert_msg == 0:
                            print_warn('Жду активные аккаунты')
                            self.update_error('#FFA200', 'Жду активные аккаунты')
                            alert_msg += 1
                        await asyncio.sleep(1)
                        continue
                    tried_accounts += 1
                    print_info(client.name)
                    if need_chat:
                        try:
                            chat = await client.join_chat(link)
                            need_chat = False
                        except FloodWait as e:
                            print_warn(f'Жду {e.value} секунд')
                            self.clients.remove(client)
                            asyncio.gather(account_waiting(self, client, e.value, self.clients))
                            await asyncio.sleep(1)
                            continue
                        except Exception:
                            chat = await client.get_chat(link)
                            need_chat = False
                    self._chats_sent[client.name] += 1
                    try:
                        await client.add_chat_members(chat_id=chat.id, user_ids=contact)
                        print_info(f'Пользователь #{counter} @{contact} приглашен')
                        self._was_invited[client.name] += 1
                        break
                    except (ChatWriteForbidden, ChannelInvalid):
                        self.update_error('red', 'ERROR (посмотри консоль)')
                        print_error('Бот должен быть админом в канале')
                        break
                    except UsernameNotOccupied:
                        print_warn(f'Контакт не существует #{counter} @{contact}')
                        break
                    except UsersTooMuch:
                        print_warn(f'У #{counter} @{contact} лимит чатов')
                        break
                    except PeerFlood:
                        print_warn('Дали спам. Пишу @SpamBot')
                        await asyncio.sleep(1)
                        await client.send_message(chat_id='SpamBot', text='/start')
                        print_info('Успешно снял спам')
                        continue
                    except FloodWait as e:
                        print_warn(f'Жду {e.value} секунд')
                        self.clients.remove(client)
                        asyncio.gather(account_waiting(self, client, e.value, self.clients))
                        await asyncio.sleep(1)
                        continue
                    except ChannelPrivate:
                        print_error('ГРУППЕ КАБЗДЕЦ')
                        self.update_error('red', 'Группе кабздец')
                        return
                    except Exception as e:
                        print(e)
                        print_error(f'Ошибка при приглашении #{counter} @{contact}')
                        await asyncio.sleep(for_sleep)
                        break
                    finally:
                        with open(('bot/database/invited_contacts.txt'), 'a') as file:
                            file.write(f'\n@{contact}')
                        invited_contacts.append(contact)
                self.clients.remove(client)
                asyncio.gather(account_waiting(self, client, abs(INVITE_DELAY - 2), self.clients))
                await asyncio.sleep(for_sleep)
            else:
                print_info(f'Уже пригласил @{contact}')
        print_info('Инвайтер закончил работу')
        self.update_error('green', f'Пригласил {counter} людей')
        self.message_invite_delay.setText('')
        with open(('bot/database/invited_contacts.txt'), 'w') as file:
            file.write('')
    except CancelledError:
        print_info('Команда отменена')
    except ZeroDivisionError:
        self.update_error('#FFA200', 'Нет активных аккаунтов')
        print_warn('Подождите, пока появятся аккаунты')
    except Exception as e:
        self.update_error('red', 'Ошибка (посмотри консоль)')
        print_error(f'Ошибка инвайтера {e}')
    self.stop.hide()
    self.chats.show()
    self.enable_items(True)