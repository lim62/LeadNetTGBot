import asyncio

from asyncio.exceptions import CancelledError
from random import uniform, choice, shuffle
from math import ceil
from redis import Redis
from aiogram.types import Message
from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors.exceptions import (
    UserAlreadyParticipant,
    FloodWait,
    ChatWriteForbidden,
    InviteRequestSent,
    SlowmodeWait,
    BadRequest,
    ChatAdminRequired,
    UsernameNotOccupied,
    InviteHashInvalid,
    InviteHashExpired,
    UsernameInvalid,
    UserBannedInChannel,
    ChannelPrivate,
    UserBlocked,
    ChatIdInvalid,
    PeerFlood,
    UserRestricted,
    ChannelsTooMuch,
)
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait as SlowmodeWaitFlood
from fluentogram import TranslatorRunner
from app.logs import print_info, print_warn, print_error
from app.services.utils import account_waiting, sending

number: int = 0

def get_next_client(clients: list[Client]) -> Client:
    global number
    number += 1
    number = 0 if number == len(clients) else number
    return clients[number]

async def process_async_groups(
    clients: list[Client],
    msg: Message,
    i18n: TranslatorRunner,
    rstorage: Redis,
    delay: int = 300
) -> None:
    global number
    number = 0
    shuffle(clients)
    old_clients: list[Client] = clients
    should_continue: bool = False
    again: bool = False
    joined: bool = False
    check_deleted: bool = False
    has_message: bool = False
    sent: int = 0
    was_sent: int = 0
    for_sleep: int = 0
    count: int = 0
    counter: int = 0
    alert_msg: int = 0
    tried_accounts: int = 0
    delay: int = 0
    first_length: int = 0
    links: list[str] = []
    used_links: list[str] = []
    valid_links: list[str] = []
    closed_topic_links: list[str] = []
    forbidden_links: list[str] = []
    invalid_links: list[str] = []
    request_links: list[str] = []
    was_deleted: list[str] = []
    bad: list[str] = []
    deleted_scanned: list[str] = []
    db: dict[str, list] = {}
    used: dict[(int, str), int] = {}
    mapped_messages: [str, bool] = {}
    chat = None
    thread_id: int = None
    try:
        while True:
            first_length = len(clients)
            delay: int = ceil(delay / first_length)
            delay = 0 if delay < 0 else delay
            with open(("bot/database/mailing/links.txt"), "r") as file:
                links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/database/mailing/used_links.txt"), "r") as file:
                used_links = [
                    used_link.strip() for used_link in file.readlines() if used_link.startswith("http")
                ]
            with open(("bot/analytics/valid_links.txt"), "r") as file:
                valid_links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/closed_topic_links.txt"), "r") as file:
                closed_topic_links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/forbidden_links.txt"), "r") as file:
                forbidden_links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/invalid_links.txt"), "r") as file:
                invalid_links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/request_links.txt"), "r") as file:
                request_links = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/was_deleted.txt"), "r") as file:
                was_deleted = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            with open(("bot/analytics/deleted_scanned.txt"), "r") as file:
                deleted_scanned = [
                    link.strip() for link in file.readlines() if link.startswith("http")
                ]
            """print_info("Собираю базу чатов...")
            if fast_mailing:
                links = []
            for client in self.clients:
                print_info(f"Собираю с {client.name}")
                db[client.name] = []
                async for dialog in client.get_dialogs():
                    if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                        if dialog.chat.username not in db[client.name]:
                            db[client.name].append(dialog.chat.username)
                            links.append(dialog.chat.username)
            print_info("Сортирую чаты")"""
            bad_links = (set(invalid_links) | set(closed_topic_links) | set(bad))
            links = [link for link in links if link not in bad_links]
            for link in links:
                if link not in used_links:
                    counter += 1
            print_info(msg, f"Неиспользованных чатов #{counter}")
            counter = 0
            while True:
                if clients:
                    client: Client = clients[0]
                    alert_msg = 0
                    break
                else:
                    if alert_msg == 0:
                        print_warn(msg, "Жду активные аккаунты")
                        alert_msg += 1
                    await asyncio.sleep(1)
                    continue
            for link in links:
                if link:
                    past_link = link if link.startswith("http") else f"https://t.me/{link}"
                    _temp = past_link.split("/")
                    if past_link not in used_links:
                        for cli in clients:
                            if past_link in db[cli.name]:
                                client = cli
                        counter += 1
                        if len(used) % 100 == 0 and len(used) != 0:
                            check_deleted = True
                        tried_accounts = 0
                        again = False
                        joined = False
                        thread_id = None
                        with open("bot/database/mailing/used_links.txt", "a") as file:
                            file.write(f"\n{past_link}")
                        used_links.append(past_link)
                        alert_msg = 0
                        while True:
                            if clients:
                                for_sleep = round(uniform(delay, delay + 1), 1) - 1.5
                                for_sleep = 0 if for_sleep < 0 else for_sleep
                                client: Client = get_next_client(clients)
                                alert_msg = 0
                                tried_accounts += 1
                            else:
                                if alert_msg == 0:
                                    print_warn(msg, "Жду активные аккаунты")
                                    alert_msg += 1
                                await asyncio.sleep(1)
                                continue
                            if (
                                past_link.startswith("https://t.me/+")
                                or past_link.startswith("http://t.me/+")
                                or past_link.startswith("https://t.me/joinchat")
                                or past_link.startswith("http://t.me/joinchat")
                                or past_link.startswith("https://t.me/c/")
                                or past_link.startswith("http://t.me/c/")
                            ):
                                link = past_link
                            elif past_link.startswith("https://t.me/") or past_link.startswith(
                                "http://t.me/"
                            ):
                                dashes: int = past_link.count("/")
                                link = past_link.split("/")[-1 - (dashes - 3)]
                            print_info(client.name)
                            sent += 1
                            try:
                                chat = await client.join_chat(link)
                                should_continue = False
                                if chat.type == ChatType.CHANNEL:
                                    if chat.linked_chat:
                                        chat = chat.linked_chat
                                        print_info(msg, f"Добавил чат #{counter}")
                                    else:
                                        print_warn(
                                            msg, f"У канала нет чата #{counter} {past_link}"
                                        )
                                        if past_link not in invalid_links:
                                            with open(
                                                "bot/analytics/invalid_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            invalid_links.append(past_link)
                                        should_continue = True
                                else:
                                    print_info(msg, f"Добавил чат #{counter}")
                                tried_accounts = 1
                                break
                            except UserAlreadyParticipant:
                                chat = await client.get_chat(link)
                                print_info(msg, f"Чат #{counter} уже добавлен")
                                should_continue = False
                                tried_accounts = 1
                                break
                            except ChannelsTooMuch:
                                print_warn(msg, "Лимит чатов достигнут")
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
                                print_info(msg, "Вышел из 10 чатов")
                                continue
                            except (UserBlocked, ChatAdminRequired, InviteHashExpired):
                                print_warn(f"Забанен в чате #{counter} {past_link}")
                                should_continue = True
                                tried_accounts = 1
                                if past_link not in forbidden_links:
                                    with open(
                                        ("bot/analytics/forbidden_links.txt"), "a"
                                    ) as file:
                                        file.write(f"\n{past_link}")
                                    forbidden_links.append(past_link)
                                break
                            except ChannelPrivate:
                                print_warn(msg, f"Чат приватный #{counter} {past_link}")
                                if past_link not in invalid_links:
                                    with open(
                                        "bot/analytics/invalid_links.txt", "a"
                                    ) as file:
                                        file.write(f"\n{past_link}")
                                    invalid_links.append(past_link)
                                tried_accounts = 1
                                should_continue = True
                                break
                            except (
                                InviteHashInvalid,
                                UsernameInvalid,
                                ChatIdInvalid,
                                UsernameNotOccupied,
                            ):
                                print_warn(msg, f"Неактивная #{counter} {past_link}")
                                if past_link not in invalid_links:
                                    with open(
                                        "bot/analytics/invalid_links.txt", "a"
                                    ) as file:
                                        file.write(f"\n{past_link}")
                                    invalid_links.append(past_link)
                                tried_accounts = 1
                                should_continue = True
                                break
                            except InviteRequestSent:
                                should_continue = True
                                for cli in old_clients:
                                    if link in db[cli.name]:
                                        client = cli
                                        joined = True
                                        print_info(
                                            msg, f"Отправлю в чат #{counter} {past_link} с {cli.name}"
                                        )
                                        asyncio.gather(
                                            send_client_wait(
                                                name=cli.name,
                                                link=link,
                                                delay=delay,
                                            )
                                        )
                                        break
                                if joined:
                                    break
                                print_warn(msg, f"Кинул заявку #{counter} {past_link}")
                                if past_link not in request_links:
                                    with open(
                                        "bot/analytics/request_links.txt", "a"
                                    ) as file:
                                        file.write(f"\n{past_link}")
                                    request_links.append(past_link)
                                tried_accounts = 1
                                break
                            except FloodWait as e:
                                print_warn(msg, f"Жду {e.value} секунд")
                                if not joined:
                                    clients.remove(client)
                                    asyncio.gather(
                                        account_waiting(client, e.value, clients)
                                    )
                                should_continue = False
                            except Exception as e:
                                text: str = str(e).lower()
                                if "frozen" in text:
                                    print_error(msg, "АККАУНТ ЗАМОРОЖЕН")
                                    try:
                                        clients.remove(client)
                                    except Exception:
                                        pass
                                    try:
                                        old_clients.remove(client)
                                    except Exception:
                                        pass
                                    first_length -= 1
                                    delay = ceil(delay / first_length)
                                elif "invalid" in text or "not found" in text:
                                    print_warn(msg, f"Забанен в чате #{counter} {past_link}")
                                    await asyncio.sleep(for_sleep)
                                    should_continue = True
                                    tried_accounts = 1
                                    if past_link not in forbidden_links:
                                        with open(
                                            ("bot/analytics/forbidden_links.txt"), "a"
                                        ) as file:
                                            file.write(f"\n{past_link}")
                                        forbidden_links.append(past_link)
                                    break
                                elif "unregistered" in text:
                                    print_error(msg, "АККАУНТ ВЫЛЕТЕЛ")
                                    try:
                                        clients.remove(client)
                                    except Exception:
                                        pass
                                    try:
                                        old_clients.remove(client)
                                    except Exception:
                                        pass
                                    first_length -= 1
                                    delay = ceil(delay / first_length)
                                    break
                                else:
                                    print(e)
                                    print_error(
                                        msg, f"Ошибка при вступлении в #{counter} {past_link}"
                                    )
                                if past_link not in invalid_links:
                                    with open(
                                        "bot/analytics/invalid_links.txt", "a"
                                    ) as file:
                                        file.write(f"\n{past_link}")
                                    invalid_links.append(past_link)
                                await asyncio.sleep(for_sleep)
                                tried_accounts = 1
                                should_continue = True
                                break
                            finally:
                                await asyncio.sleep(choice([1, 1.2, 1.4]))
                        if should_continue:
                            clients.remove(client)
                            asyncio.gather(
                                account_waiting(
                                    client, abs(delay - 2), clients
                                )
                            )
                            await asyncio.sleep(for_sleep)
                            continue
                        should_continue = False
                        has_message = False
                        if chat and chat.id:
                            async for message in client.get_chat_history("me", limit=1):
                                has_message = True
                                while True:
                                    tried_accounts += 1
                                    if again:
                                        client: Client = choice(clients)
                                        try:
                                            chat = await client.join_chat(chat.id)
                                        except UserAlreadyParticipant:
                                            chat = await client.get_chat(chat.id)
                                        except Exception:
                                            break
                                        await asyncio.sleep(choice([1, 1.2, 1.4]))
                                        print_info(client.name)
                                    try:
                                        id = await sending(
                                            client=client,
                                            message=message,
                                            chat=chat,
                                            reply_id=thread_id,
                                        )
                                        print_info(msg, f"Отправил в чат #{counter} {past_link}")
                                        used[(link, past_link)] = id
                                        was_sent[client.name] += 1
                                        count += 1
                                        if past_link not in valid_links:
                                            with open(
                                                "bot/analytics/valid_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            valid_links.append(past_link)
                                        break
                                    except ChatWriteForbidden:
                                        print_warn(msg, f"Забанен в #{counter} {past_link}")
                                        if past_link not in forbidden_links:
                                            with open(
                                                "bot/analytics/forbidden_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            forbidden_links.append(past_link)
                                        should_continue = True
                                        break
                                    except BadRequest as e:
                                        text = str(e).lower()
                                        if "spam" in text:
                                            print_warn(
                                                msg, f"{client.name} дали спам. Пишу @SpamBot"
                                            )
                                            await asyncio.sleep(0.5)
                                            await client.send_message(
                                                chat_id="SpamBot", text="/start"
                                            )
                                            print_info(msg, "Успешно снял спам")
                                            if past_link not in valid_links:
                                                with open(
                                                    "bot/analytics/valid_links.txt", "a"
                                                ) as file:
                                                    file.write(f"\n{past_link}")
                                                valid_links.append(past_link)
                                            if tried_accounts > 3:
                                                print_error(msg, "Ошибка в аккаунте")
                                                clients.remove(client)
                                                again = True
                                            continue
                                        elif "closed" in text:
                                            print_warn(
                                                msg, f"Тема закрыта #{counter} {past_link}"
                                            )
                                            should_continue = True
                                            if past_link not in closed_topic_links:
                                                with open(
                                                    "bot/analytics/closed_topic_links.txt",
                                                    "a",
                                                ) as file:
                                                    file.write(f"\n{past_link}")
                                                closed_topic_links.append(past_link)
                                            if past_link not in invalid_links:
                                                with open(
                                                    "bot/analytics/invalid_links.txt", "a"
                                                ) as file:
                                                    file.write(f"\n{past_link}")
                                                invalid_links.append(past_link)
                                        elif 'required' in text:
                                            print_warn(
                                                msg, f"Запрещено писать #{counter} {past_link}"
                                            )
                                            if past_link not in invalid_links:
                                                with open(
                                                    msg, "bot/analytics/invalid_links.txt", "a"
                                                ) as file:
                                                    file.write(f"\n{past_link}")
                                                invalid_links.append(past_link)
                                        else:
                                            print_warn(msg, f'Ошибка при отправке {e}')
                                        break
                                    except (SlowmodeWait, SlowmodeWaitFlood) as e:
                                        print_info(
                                            msg, f"Отправлю через {e.value} #{counter} {past_link}"
                                        )
                                        asyncio.gather(
                                            process_delay_sending(
                                                client,
                                                chat,
                                                message,
                                                e.value,
                                                past_link,
                                                invalid_links,
                                                valid_links,
                                            )
                                        )
                                        break
                                    except (UserBannedInChannel, PeerFlood, UserRestricted):
                                        print_warn(msg, "Дали спам. Пишу @SpamBot")
                                        await asyncio.sleep(0.5)
                                        await client.send_message(
                                            chat_id="SpamBot", text="/start"
                                        )
                                        print_info(msg, "Успешно снял спам")
                                        if past_link not in valid_links:
                                            with open(
                                                "bot/analytics/valid_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            valid_links.append(past_link)
                                        if tried_accounts > 3:
                                            print_error(msg, "Ошибка в аккаунте")
                                            clients.remove(client)
                                            again = True
                                        await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                        continue
                                    except FloodWait as e:
                                        print_warn(msg, f"Жду {e.value} секунд")
                                        if past_link not in valid_links:
                                            with open(
                                                "bot/analytics/valid_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            valid_links.append(past_link)
                                        clients.remove(client)
                                        asyncio.gather(
                                            account_waiting(
                                                client, e.value, clients
                                            )
                                        )
                                        break
                                    except Exception as e:
                                        text: str = str(e).lower()
                                        if "private" in text:
                                            print_warn(
                                                msg, f"Чат приватный #{counter} {past_link}"
                                            )
                                        elif "payment" in text:
                                            print_warn(
                                                msg, f"Запрещено писать #{counter} {past_link}"
                                            )
                                        elif "forbidden" in text:
                                            print_warn(msg, f"Забанен в чате #{counter} {past_link}")
                                            if past_link not in forbidden_links:
                                                with open(
                                                    "bot/analytics/forbidden_links.txt", "a"
                                                ) as file:
                                                    file.write(f"\n{past_link}")
                                                forbidden_links.append(past_link)
                                            break
                                        else:
                                            print(e)
                                            print_error(
                                                msg, f"Ошибка при отправке в #{counter} {past_link}"
                                            )
                                        should_continue = True
                                        if past_link not in invalid_links:
                                            with open(
                                                "bot/analytics/invalid_links.txt", "a"
                                            ) as file:
                                                file.write(f"\n{past_link}")
                                            invalid_links.append(past_link)
                                        break
                            if not has_message:
                                print_error(msg, 'НЕТ ОФФЕРА')
                                try:
                                    clients.remove(client)
                                except Exception:
                                    pass
                                try:
                                    old_clients.remove(client)
                                except Exception:
                                    pass
                                first_length -= 1
                                delay = ceil(delay / first_length)
                        else:
                            print_warn(msg, f"Не удалось получить чат {past_link}")
                        if client in clients:
                            clients.remove(client)
                            asyncio.gather(
                                account_waiting(client, (delay - 4), clients)
                            )
                        if should_continue:
                            await asyncio.sleep(for_sleep)
                            continue
                        asyncio.gather(
                            chat_leaving(client, chat, counter, choice([5, 10, 20]))
                        )
                        print_info(msg, f'Вышел из чата #{counter}')
                        await asyncio.sleep(for_sleep)
                        if check_deleted:
                            print_info(msg, "Сканирую удаленные сообщения...")
                            await asyncio.sleep(delay)
                            for used_chat, message_id in used.items():
                                id: str = used_chat[0]
                                link: str = used_chat[1]
                                if link not in deleted_scanned:
                                    client = get_next_client(clients)
                                    try:
                                        print_info(msg, f"Сканирую {link}")
                                        await client.join_chat(id)
                                        await asyncio.sleep(delay)
                                        message = await client.get_messages(
                                            id, message_id
                                        )
                                    except Exception:
                                        continue
                                    mapped_messages[link] = (
                                        True if message and not message.empty else False
                                    )
                                    deleted_scanned.append(link)
                                    with open(
                                        ("bot/analytics/deleted_scanned.txt"), "a"
                                    ) as file:
                                        file.write(f"\n{link}")
                            with open("bot/analytics/was_deleted.txt", "a") as file:
                                for link, value in mapped_messages.items():
                                    if not value:
                                        if link not in was_deleted:
                                            file.write(f"\n{link}")
                                            was_deleted.append(link)
                            used = {}
                            check_deleted = False
                            await asyncio.sleep(delay / 2)
                            print_info(msg, "Сканирование завершено")
                    else:
                        print_info(msg, f"Уже отправил в чат {link}")
            print_info(msg, "Продолжаю по кругу...")
            with open(("bot/database/mailing/used_links.txt"), "w") as file:
                file.write("")
            used_links = []
            await asyncio.sleep(delay + 1)
    except CancelledError:
        print_info("Команда отменена")
    except Exception as e:
        print(e)
        print_error(msg, f"Ошибка при выполнении рассылки по группам: {e}")

async def chat_leaving(client: Client, chat: any, delay: float) -> None:
    await asyncio.sleep(delay)
    try:
        await client.leave_chat(chat.id)
    except Exception:
        pass

async def process_delay_sending(
    client: Client,
    chat: any,
    message: any,
    delay: float,
    past_link: str,
    invalid_links: list[str],
    valid_links: list[str],
) -> None:
    await asyncio.sleep(delay + 1)
    try:
        await sending(client, message, chat)
        if past_link not in valid_links:
            with open("bot/analytics/valid_links.txt", "a") as file:
                file.write(f"\n{past_link}")
            valid_links.append(past_link)
    except Exception:
        if past_link not in invalid_links:
            with open("bot/analytics/invalid_links.txt", "a") as file:
                file.write(f"\n{past_link}")
            invalid_links.append(past_link)


async def send_client_wait(clients: list[Client], name: str, link: str, delay: int) -> None:
    client: Client
    counter: int = 0
    while True:
        counter += 1
        for client in clients:
            if client.name == name:
                try:
                    chat = await client.join_chat(link)
                    async for message in client.get_chat_history("me", limit=1):
                        await sending(client=client, message=message, chat=chat)
                except Exception:
                    pass
                return
        await asyncio.sleep(delay / 10)
        if counter >= int(delay / 6):
            return