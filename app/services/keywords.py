import asyncio

from random import shuffle, choice
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from asyncio.exceptions import CancelledError
from pyrogram import Client
from pyrogram.types import Message, Chat
from pyrogram.enums import ParseMode, ChatType
from pyrogram.errors import (UserAlreadyParticipant, ChannelsTooMuch, ChannelPrivate,
                             UserBlocked, ChatAdminRequired, InviteHashExpired,
                             InviteHashInvalid, UsernameInvalid, ChatIdInvalid,
                             UsernameNotOccupied, BadRequest, InviteRequestSent,
                             UserBannedInChannel, PeerFlood, UserRestricted,
                             FloodWait)
from bot.logs import print_info, print_warn, print_error
from bot.services.utils import account_waiting

if TYPE_CHECKING:
    from app.qt_windows.bot_window import BotWindow

async def parsing(
    self: 'BotWindow',
    message: Message,
    client: Client,
    chat: Chat,
    keyword: str,
    result_messages: dict,
    used_text: list[str],
    collected_links: list[str],
    bad_keywords: list[str],
    bad_links: list[str]
) -> None:
    text: str = ''
    link: str = ''
    past_text: str = ''
    to_add: tuple = ()
    if message.from_user and message.from_user.username:
        if message.chat and message.chat.username:
            if message.text or message.caption:
                try:
                    link = f'https://t.me/{message.chat.username}'
                    if link not in bad_links:
                        link += f'/{message.id}'
                        text = message.text if message.text else message.caption
                        past_text = text
                        text = text.lower()[:25].replace('\n', ' ')
                        if link not in collected_links:
                            with open(('bot/database/keywords/collected_links.txt'), 'a', encoding='utf8') as file:
                                file.write(f'\n{link}')
                            collected_links.append(link)
                            if text not in used_text:
                                with open(('bot/database/keywords/used_text.txt'), 'a', encoding='utf8') as file:
                                    file.write(f'\n{text}')
                                    used_text.append(text)
                                date_now = datetime.now()
                                msg_date = message.date
                                difference: timedelta = date_now - msg_date
                                if difference < timedelta(days=3) and 'bot' not in message.from_user.username.lower():
                                    for bad_keyword in bad_keywords:
                                        if bad_keyword in past_text:
                                            return
                                    to_add = (message.from_user.username, text, link)
                                    if to_add not in result_messages[keyword]:
                                        result_messages[keyword].append(to_add)
                                        print_info(f'Отправляю {message.chat.username}/{message.id}')
                                        text = f'⚡ <b>NEW LEAD</b> ⚡\n\n<b>Keyword:</b> <u>{keyword}</u>\n\n<b>Username:</b> @{message.from_user.username}\n\n<b>Text:</b> {past_text[:800]}\n\n<b>Date: </b>{msg_date}\n<b>Link:</b> {link}'
                                        await client.send_animation(
                                            chat_id=chat.id,
                                            animation='https://t.me/sksjkdksnsjdjdndksm/7',
                                            caption=text,
                                            parse_mode=ParseMode.HTML
                                        )
                except FloodWait as e:
                    print_warn(f"Жду {e.value} секунд")
                    self.clients.remove(client)
                    asyncio.gather(
                        account_waiting(self, client, e.value, self.clients)
                    )
                except Exception as e:
                    print_error(f'Ошибка парсинга {e}')

async def proccess_keywords(self: 'BotWindow', DELAY: int) -> None:
    print_info('Collector начал работу')
    shuffle(self.clients)
    ID: int = 'https://t.me/+ALAtgKBOmRlkYWYy'
    counter: int = 0
    alert_msg: int = 0
    delay: int = int(DELAY / len(self.clients))
    delay = delay if delay >= 1 else 1
    keywords: list[str] = []
    bad_keywords: list[str] = []
    result_messages: dict[str, (str, str, str)] = {}
    is_open: bool = False
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
        with open(('bot/database/keywords/keywords.txt'), 'r', encoding='utf8') as file:
            keywords = [
                keyword.strip() for keyword in file.readlines() if keyword
            ]
        with open(('bot/database/keywords/bad_keywords.txt'), 'r', encoding='utf8') as file:
            bad_keywords = [
                keyword.strip() for keyword in file.readlines() if keyword
            ]
        with open(("bot/database/mailing/links.txt"), "r", encoding='utf8') as file:
            links = [
                link.strip() for link in file.readlines() if link.startswith("http")
            ]
        with open(("bot/database/keywords/bad_links.txt"), "r", encoding='utf8') as file:
            bad = [
                link.strip() for link in file.readlines() if link.startswith("http")
            ]
        with open(("bot/database/keywords/collected_links.txt"), "r", encoding='utf8') as file:
            collected_links = [
                collected_link.strip() for collected_link in file.readlines() if collected_link.startswith('http')
            ]
        with open(("bot/database/keywords/used_text.txt"), "r", encoding='utf8') as file:
            used_text = [
                used.strip() for used in file.readlines() if used
            ]
        with open(("bot/analytics/forbidden_links.txt"), "r", encoding='utf8') as file:
            forbidden_links = [
                link.strip() for link in file.readlines() if link.startswith("http")
            ]
        with open(("bot/analytics/invalid_links.txt"), "r", encoding='utf8') as file:
            invalid_links = [
                link.strip() for link in file.readlines() if link.startswith("http")
            ]
        with open(("bot/analytics/request_links.txt"), "r", encoding='utf8') as file:
            request_links = [
                link.strip() for link in file.readlines() if link.startswith("http")
            ]
        bad_links: set = set(forbidden_links) | set(invalid_links) | set(request_links)
        links = [link for link in links if link not in bad_links]
        for keyword in keywords:
            result_messages[keyword] = []
        print_info('Собираю с Global:')
        for client in self.clients:
            try:
                main_chat = await client.join_chat(ID)
            except UserAlreadyParticipant:
                main_chat = await client.get_chat(ID)
            except Exception as e:
                print(client.name)
                print_error(f'Ошибка вступления {e}')
                raise CancelledError()
        for client in self.clients:
            print_info(client.name)
            for keyword in keywords:
                self._was_lead[client.name] += 1
                print_info(f'Cобираю "{keyword}"')
                try:
                    async for message in client.search_global(query=keyword, limit=50):
                        await parsing(
                            self=self,
                            message=message,
                            client=client,
                            chat=main_chat,
                            keyword=keyword,
                            result_messages=result_messages,
                            used_text=used_text,
                            collected_links=collected_links,
                            bad_keywords=bad_keywords,
                            bad_links=bad
                        )
                        await asyncio.sleep(0.1)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    print_warn(f"Жду {e.value} секунд")
                    self.clients.remove(client)
                    asyncio.gather(
                        account_waiting(self, client, e.value, self.clients)
                    )
                except Exception as e:
                    print_error(f'Ошибка Global {e}')
            await asyncio.sleep(delay)
        print_info('Собираю с Usual:')
        for link in links:
            if link not in collected_links:
                counter += 1
        print_info(f"Неиспользованных чатов #{counter}")
        counter = 0
        while True:
            for link in links:
                counter += 1
                client = self.get_next_client(self.clients)
                print_info(client.name)
                print_info(f'Собираю #{counter} с {link}')
                is_open = False
                past_link = link if link.startswith("http") else f"https://t.me/{link}"
                if past_link not in collected_links:
                    if (
                        past_link.startswith("https://t.me/+")
                        or past_link.startswith("http://t.me/+")
                        or past_link.startswith("https://t.me/joinchat")
                        or past_link.startswith("http://t.me/joinchat")
                        or past_link.startswith("https://t.me/c/")
                        or past_link.startswith("http://t.me/c/")
                    ):
                        link = past_link
                    elif past_link.startswith("https://t.me/") or past_link.startswith("http://t.me/"):
                        is_open = True
                        dashes: int = past_link.count("/")
                        link = past_link.split("/")[-1 - (dashes - 3)]
                    if not is_open:
                        try:
                            chat = await client.join_chat(link)
                        except UserAlreadyParticipant:
                            chat = await client.get_chat(link)
                        except ChannelsTooMuch:
                            print_warn("Лимит чатов достигнут")
                            to_leave = 0
                            async for dialog in client.get_dialogs():
                                if to_leave >= 10:
                                    break
                                if dialog.chat.type in (
                                    ChatType.GROUP,
                                    ChatType.SUPERGROUP,
                                    ChatType.CHANNEL,
                                ):
                                    if (
                                        dialog.chat.username
                                        and "leadnet" not in dialog.chat.username.lower()
                                    ):
                                        await client.leave_chat(dialog.chat.id)
                                        await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                        to_leave += 1
                                print_info("Вышел из 10 чатов")
                                continue
                        except Exception as e:
                            print_error(f'Ошибка при вступлении {e}')
                            continue
                    try:
                        for keyword in keywords:
                            self._was_lead[client.name] += 1
                            print_info(f'Cобираю "{keyword}"')
                            async for message in client.search_messages(chat_id=link, query=keyword, limit=20):
                                await parsing(
                                    self=self,
                                    message=message,
                                    client=client,
                                    chat=main_chat,
                                    keyword=keyword,
                                    result_messages=result_messages,
                                    used_text=used_text,
                                    collected_links=collected_links,
                                    bad_keywords=bad_keywords,
                                    bad_links=bad
                                )
                                await asyncio.sleep(0.1)
                            await asyncio.sleep(0.5)
                    
                    except (UserBlocked, ChatAdminRequired, InviteHashExpired):
                        print_warn(f"Забанен в чате {past_link}")
                        if past_link not in forbidden_links:
                            with open(
                                ("bot/analytics/forbidden_links.txt"), "a"
                            ) as file:
                                file.write(f"\n{past_link}")
                            forbidden_links.append(past_link)
                        break
                    except ChannelPrivate:
                        print_warn(f"Чат приватный #{counter} {past_link}")
                        if past_link not in invalid_links:
                            with open(
                                "bot/analytics/invalid_links.txt", "a"
                            ) as file:
                                file.write(f"\n{past_link}")
                            invalid_links.append(past_link)
                    except (
                        InviteHashInvalid,
                        UsernameInvalid,
                        ChatIdInvalid,
                        UsernameNotOccupied
                    ):
                        print_warn(f"Неактивная #{counter} {past_link}")
                        if past_link not in invalid_links:
                            with open(
                                "bot/analytics/invalid_links.txt", "a"
                            ) as file:
                                file.write(f"\n{past_link}")
                            invalid_links.append(past_link)
                    except InviteRequestSent:
                        print_warn(f"Кинул заявку #{counter} {past_link}")
                    except BadRequest as e:
                        text = str(e).lower()
                        if "spam" in text:
                            print_warn(
                                f"{client.name} дали спам. Пишу @SpamBot"
                            )
                            await asyncio.sleep(0.5)
                            await client.send_message(
                                chat_id="SpamBot", text="/start"
                            )
                            print_info("Успешно снял спам")
                    except (UserBannedInChannel, PeerFlood, UserRestricted):
                        print_warn("Дали спам. Пишу @SpamBot")
                        await asyncio.sleep(0.5)
                        await client.send_message(
                            chat_id="SpamBot", text="/start"
                        )
                        print_info("Успешно снял спам")
                    except FloodWait as e:
                        print_warn(f"Жду {e.value} секунд")
                        self.clients.remove(client)
                        asyncio.gather(
                            account_waiting(
                                self, client, e.value, self.clients
                            )
                        )
                    except Exception as e:
                        text: str = str(e).lower()
                        if "private" in text:
                            print_warn(
                                f"Чат приватный #{counter} {past_link}"
                            )
                        elif "payment" in text:
                            print_warn(
                                f"Запрещено писать #{counter} {past_link}"
                            )
                        elif "forbidden" in text or 'expired' in text:
                            print_warn(f"Забанен в #{counter} {past_link}")
                            if past_link not in forbidden_links:
                                with open(
                                    "bot/analytics/forbidden_links.txt", "a"
                                ) as file:
                                    file.write(f"\n{past_link}")
                                forbidden_links.append(past_link)
                            break
                        if "frozen" in text:
                            print_error("АККАУНТ ЗАМОРОЖЕН")
                            if client in self.clients:
                                self.clients.remove(client)
                        elif "invalid" in text or "not found" in text:
                            print_warn(f"Забанен в чате {past_link}")
                            if past_link not in forbidden_links:
                                with open(
                                    ("bot/analytics/forbidden_links.txt"), "a"
                                ) as file:
                                    file.write(f"\n{past_link}")
                                forbidden_links.append(past_link)
                        elif "unregistered" in text:
                            print_error("АККАУНТ ВЫЛЕТЕЛ")
                            if client in self.clients:
                                self.clients.remove(client)
                    if not is_open:
                        try:
                            await client.leave_chat(chat.id)
                        except Exception:
                            pass
                    await asyncio.sleep(delay)
            collected_links = []
            shuffle(self.clients)
            counter = 0
    except CancelledError:
        print_info('Команда отменена')
    except Exception as e:
        self.update_error('red', 'Ошибка (посмотри консоль)')
        print_error(f'Ошибка Collector {e}')
    self.stop.hide()
    self.chats.show()
    self.enable_items(True)