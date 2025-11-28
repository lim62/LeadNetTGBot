import asyncio

from math import ceil
from random import choice, shuffle, uniform
from asyncio.exceptions import CancelledError
from typing import TYPE_CHECKING
from pyrogram import Client
from pyrogram.errors import (FloodWait, BadRequest, UserBannedInChannel,
                             PeerFlood, UserRestricted, MessageEmpty)
from bot.logs import print_info, print_warn, print_error
from bot.services.utils import account_waiting, sending

if (TYPE_CHECKING):
    from app.qt_windows.bot_window import BotWindow

async def process_async_private(
    self: "BotWindow", MESSAGE_DELAY: int = 120
) -> None:
    print_info("Началась рассылка по личкам")
    shuffle(self.clients)
    tried_accounts: int = 0
    count: int = 0
    counter: int = 0
    contacts: list[str] = []
    used_contacts: list[str] = []
    has_message: bool = False
    again: bool = False
    while True:
        if self.clients:
            client: Client = self.clients[0]
            self.update_error("green", "Выполняю...")
            alert_msg = 0
            break
        else:
            if alert_msg == 0:
                print_warn("Жду активные аккаунты")
                self.update_error("#FFA200", "Жду активные аккаунты")
                alert_msg += 1
            await asyncio.sleep(1)
            continue
    try:
        counter = 0
        first_length = len(self.clients)
        delay: int = ceil(MESSAGE_DELAY / first_length)
        delay = 0 if delay < 0 else delay
        with open(("bot/database/private_mailing/contacts.txt"), "r") as file:
            contacts = [
                contact.strip()[1:] for contact in file.readlines() if contact.startswith("@")
            ]
        with open(("bot/database/private_mailing/used_contacts.txt"), "r") as file:
            used_contacts = [
                used_contact.strip()[1:] for used_contact in file.readlines() if used_contact.startswith("@")
            ]
        while True:
            if self.clients:
                client: Client = self.clients[0]
                self.update_error("green", "Выполняю...")
                alert_msg = 0
                break
            else:
                if alert_msg == 0:
                    print_warn("Жду активные аккаунты")
                    self.update_error("#FFA200", "Жду активные аккаунты")
                    alert_msg += 1
                await asyncio.sleep(1)
                continue
        for contact in contacts:
            if contact not in used_contacts:
                counter += 1
                tried_accounts = 0
                has_message = False
                again = False
                with open("bot/database/private_mailing/used_contacts.txt", "a") as file:
                    file.write(f"\n@{contact}")
                used_contacts.append(contact)
                alert_msg = 0
                while True:
                    if self.clients:
                        for_sleep = round(uniform(delay, delay + 1), 1) - 1.5
                        for_sleep = 0 if for_sleep < 0 else for_sleep
                        client: Client = self.get_next_client(self.clients)
                        self.update_error("green", "Выполняю...")
                        alert_msg = 0
                        break
                    else:
                        if alert_msg == 0:
                            print_warn("Жду активные аккаунты")
                            self.update_error("#FFA200", "Жду активные аккаунты")
                            alert_msg += 1
                        await asyncio.sleep(1)
                        continue
                print_info(client.name)
                self._private_sent[client.name] += 1
                try:
                    async for message in client.get_chat_history("me", limit=1):
                        has_message = True
                        while True:
                            if again:
                                client: Client = choice(self.clients)
                                print_info(client.name)
                            try:
                                tried_accounts += 1
                                await sending(
                                    client=client,
                                    message=message,
                                    chat=contact
                                )
                                print_info(f"Отправил в #{counter} @{contact}")
                                self._was_private_sent[client.name] += 1
                                count += 1
                                break
                            except BadRequest as e:
                                text = str(e).lower()
                                if "spam" in text or 'peer' in text:
                                    print_warn(
                                        f"{client.name} дали спам. Пишу @SpamBot"
                                    )
                                    await asyncio.sleep(0.5)
                                    await client.send_message(
                                        chat_id="SpamBot", text="/start"
                                    )
                                    print_info("Успешно снял спам")
                                    if tried_accounts > 3:
                                        print_error("Ошибка в аккаунте")
                                        self.clients.remove(client)
                                        again = True
                                    await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                    continue
                                elif 'empty' in text:
                                    print_warn("Дали спам. Пишу @SpamBot")
                                    await asyncio.sleep(0.5)
                                    await client.send_message(
                                        chat_id="SpamBot", text="/start"
                                    )
                                    print_info("Успешно снял спам")
                                    if tried_accounts > 3:
                                        print_error("Ошибка в аккаунте")
                                        self.clients.remove(client)
                                        again = True
                                    await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                    continue
                                elif 'required' in text:
                                    print_warn(
                                        f"Запрещено писать #{counter} {contact}"
                                    )
                                else:
                                    print_error(f'Ошибка при отправке {e}')
                                break
                            except (UserBannedInChannel, PeerFlood, UserRestricted, MessageEmpty):
                                print_warn("Дали спам. Пишу @SpamBot")
                                await asyncio.sleep(0.5)
                                await client.send_message(
                                    chat_id="SpamBot", text="/start"
                                )
                                print_info("Успешно снял спам")
                                if tried_accounts > 3:
                                    print_error("Ошибка в аккаунте")
                                    self.clients.remove(client)
                                    again = True
                                await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                continue
                            except FloodWait as e:
                                print_warn(f"Жду {e.value} секунд")
                                self.clients.remove(client)
                                asyncio.gather(
                                    account_waiting(
                                        self, client, e.value, self.clients
                                    )
                                )
                                await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                if tried_accounts <= len(self._available_clients):
                                    again = True
                                    continue
                                else:
                                    break
                            except Exception as e:
                                text: str = str(e).lower()
                                if "payment" in text:
                                    print_warn(
                                        f"Запрещено писать #{counter} {contact}"
                                    )
                                elif "forbidden" in text:
                                    print_warn(f"Забанен в #{counter} {contact}")
                                    break
                                else:
                                    print(e)
                                    print_error(
                                        f"Ошибка при отправке в #{counter} {contact}"
                                    )
                                break
                except Exception as e:
                    print_error(f'Ошибка при отправке {e}')
                if not has_message:
                    print_error('НЕТ ОФФЕРА')
                    try:
                        self.clients.remove(client)
                    except Exception:
                        pass
                    first_length -= 1
                    delay = ceil(MESSAGE_DELAY / first_length)
                await asyncio.sleep(for_sleep)
            else:
                print_info(f'Уже отправлено @{contact}')
        print_info(f"Отправил в {count} чатов")
        print_info('Рассылка закончена')
        self.update_error("green", f'Отправил в {count} чатов')
        with open(("bot/database/private_mailing/used_contacts.txt"), "w") as file:
            file.write("")
        used_contacts = []
    except CancelledError:
        print_info("Команда отменена")
    except Exception as e:
        self.update_error("red", "Ошибка (посмотри консоль)")
        print(e)
        print_error(f"Ошибка при выполнении рассылки по личкам: {e}")
    self.stop.hide()
    self.chats.show()
    self.enable_items(True)