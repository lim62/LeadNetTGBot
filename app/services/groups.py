import asyncio

from asyncio.exceptions import CancelledError
from redis import Redis
from random import uniform, choice, shuffle
from math import ceil
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
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.logs import print_info, print_warn, print_error
from app.services.utils import account_waiting, sending, get_next_client, deleting_account
from bot.keyboards import get_workpulse_kbd


async def process_async_groups(
    old_clients: list[Client],
    msg: Message,
    telegram_id: int,
    i18n: TranslatorRunner,
    rstorage: Redis,
    session_maker: async_sessionmaker,
    MESSAGE_DELAY: int = 300,
    have_logs: bool = True,
    for_all: bool = False,
    from_zalp: bool = False
) -> None:
    new_clients: list[Client] = old_clients
    shuffle(new_clients)
    await rstorage.set(f'lencli{telegram_id}', 0)
    should_continue: bool = False
    again: bool = False
    was_delayed: bool = False
    has_message: bool = False
    sent: int = 0
    was_sent: int = 0
    for_sleep: int = 0
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
    bad: list[str] = []
    db: dict[str, list] = {}
    chat = None
    thread_id: int = None
    try:
        delay: int = ceil(MESSAGE_DELAY / len(new_clients))
        delay = 0 if delay == 1 else delay
        with open((f"app/database/groups/links{telegram_id}.txt"), "r") as file:
            links = [link.strip() for link in file.readlines() if link.startswith("http")]
        with open((f"app/database/groups/used_links{telegram_id}.txt"), "r") as file:
            used_links = [used_link.strip() for used_link in file.readlines() if used_link.startswith("http")]
        with open(("app/analytics/valid_links.txt"), "r") as file:
            valid_links = [link.strip() for link in file.readlines() if link.startswith("http")]
        with open(("app/analytics/closed_topic_links.txt"), "r") as file:
            closed_topic_links = [link.strip() for link in file.readlines() if link.startswith("http")]
        with open(("app/analytics/forbidden_links.txt"), "r") as file:
            forbidden_links = [link.strip() for link in file.readlines() if link.startswith("http")]
        with open(("app/analytics/invalid_links.txt"), "r") as file:
            invalid_links = [link.strip() for link in file.readlines() if link.startswith("http")]
        with open(("app/analytics/request_links.txt"), "r") as file:
            request_links = [link.strip() for link in file.readlines() if link.startswith("http")]
        await print_info(msg, "Собираю базу чатов...", have_logs)
        if for_all:
            links = []
        if not from_zalp:
            for client in new_clients:
                await print_info(msg, f"Собираю с {client.name}", have_logs)
                db[client.name] = []
                async for dialog in client.get_dialogs():
                    if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                        if dialog.chat.username not in db[client.name]:
                            db[client.name].append(dialog.chat.username)
                            if for_all:
                                links.append(f'https://t.me/{dialog.chat.username}')
        await print_info(msg, "Сортирую чаты", have_logs)
        if not from_zalp:
            bad_links = (set(invalid_links) | set(closed_topic_links) | set(bad))
            links = [link for link in links if link not in bad_links]
        for link in links:
            if link not in used_links:
                counter += 1
        await print_info(msg, f"Неиспользованных чатов #{counter}", have_logs)
        counter = 0
        while True:
            if new_clients:
                client: Client = new_clients[0]
                alert_msg = 0
                break
            else:
                if alert_msg == 0:
                    await print_warn(msg, "Жду активные аккаунты", have_logs)
                    alert_msg += 1
                await asyncio.sleep(1)
                continue
        for link in links:
            if link:
                past_link = link if link.startswith("http") else f"https://t.me/{link}"
                _temp = past_link.split("/")
                if past_link not in used_links:
                    if not from_zalp:
                        for cli in new_clients:
                            if past_link in db[cli.name]:
                                client = cli
                    counter += 1
                    tried_accounts = 0
                    again = False
                    was_delayed = False
                    thread_id = None
                    with open(f"app/database/groups/used_links{telegram_id}.txt", "a") as file:
                        file.write(f"\n{past_link}")
                    used_links.append(past_link)
                    alert_msg = 0
                    while True:
                        if new_clients:
                            for_sleep = uniform(delay, delay + 1) - 1.5
                            for_sleep = 0 if for_sleep <= 1 else for_sleep
                            client: Client = await get_next_client(
                                clients=new_clients,
                                rstorage=rstorage,
                                telegram_id=telegram_id
                            )
                            alert_msg = 0
                            tried_accounts += 1
                        else:
                            if alert_msg == 0:
                                await print_warn(msg, "Жду активные аккаунты", have_logs)
                                alert_msg += 1
                            await asyncio.sleep(1)
                            continue
                        if (past_link.startswith("https://t.me/+") or past_link.startswith("http://t.me/+") or past_link.startswith("https://t.me/joinchat") or past_link.startswith("http://t.me/joinchat") or past_link.startswith("https://t.me/c/") or past_link.startswith("http://t.me/c/")):
                            link = past_link
                        elif past_link.startswith("https://t.me/") or past_link.startswith("http://t.me/"):
                            dashes: int = past_link.count("/")
                            link = past_link.split("/")[-1 - (dashes - 3)]
                        sent += 1
                        try:
                            chat = await client.join_chat(link)
                            should_continue = False
                            if chat.type == ChatType.CHANNEL:
                                if chat.linked_chat:
                                    chat = chat.linked_chat
                                    await print_info(msg, f"Добавил чат #{counter}", have_logs)
                                else:
                                    await print_warn(msg, f"У канала нет чата #{counter} {past_link}", have_logs)
                                    if past_link not in invalid_links:
                                        with open("app/analytics/invalid_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        invalid_links.append(past_link)
                                    should_continue = True
                            else:
                                await print_info(msg, f"Добавил чат #{counter}", have_logs)
                            tried_accounts = 1
                            break
                        except UserAlreadyParticipant:
                            chat = await client.get_chat(link)
                            await print_info(msg, f"Чат #{counter} уже добавлен", have_logs)
                            should_continue = False
                            tried_accounts = 1
                            break
                        except ChannelsTooMuch:
                            await print_warn(msg, "Лимит чатов достигнут", have_logs)
                            to_leave = 0
                            async for dialog in client.get_dialogs():
                                if to_leave >= 10:
                                    break
                                if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL):
                                    if dialog.chat.username:
                                        await client.leave_chat(dialog.chat.id)
                                        await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                        to_leave += 1
                            await print_info(msg, "Вышел из 10 чатов", have_logs)
                            continue
                        except (UserBlocked, ChatAdminRequired, InviteHashExpired):
                            await print_warn(msg, f"Забанен в чате #{counter} {past_link}", have_logs)
                            should_continue = True
                            tried_accounts = 1
                            if past_link not in forbidden_links:
                                with open(("app/analytics/forbidden_links.txt"), "a") as file:
                                    file.write(f"\n{past_link}")
                                forbidden_links.append(past_link)
                            break
                        except ChannelPrivate:
                            await print_warn(msg, f"Чат приватный #{counter} {past_link}", have_logs)
                            if past_link not in invalid_links:
                                with open("app/analytics/invalid_links.txt", "a") as file:
                                    file.write(f"\n{past_link}")
                                invalid_links.append(past_link)
                            tried_accounts = 1
                            should_continue = True
                            break
                        except (InviteHashInvalid, UsernameInvalid, ChatIdInvalid, UsernameNotOccupied,):
                            await print_warn(msg, f"Неактивная #{counter} {past_link}", have_logs)
                            if past_link not in invalid_links:
                                with open("app/analytics/invalid_links.txt", "a") as file:
                                    file.write(f"\n{past_link}")
                                invalid_links.append(past_link)
                            tried_accounts = 1
                            should_continue = True
                            break
                        except InviteRequestSent:
                            should_continue = True
                            await print_warn(msg, f"Кинул заявку #{counter} {past_link}", have_logs)
                            if past_link not in request_links:
                                with open("app/analytics/request_links.txt", "a") as file:
                                    file.write(f"\n{past_link}")
                                request_links.append(past_link)
                            tried_accounts = 1
                            break
                        except FloodWait as e:
                            await print_warn(msg, f"Жду {e.value} секунд", have_logs)
                            new_clients.remove(client)
                            asyncio.gather(account_waiting(client, e.value, new_clients))
                            was_delayed = True
                            should_continue = True
                        except Exception as e:
                            text: str = str(e).lower()
                            if "frozen" in text:
                                await print_error(msg, "АККАУНТ ЗАМОРОЖЕН", have_logs)
                                await deleting_account(
                                    client=client,
                                    clients=new_clients,
                                    old_clients=old_clients,
                                    session_maker=session_maker
                                )
                                first_length -= 1
                                delay = ceil(delay / first_length)
                            elif "invalid" in text or "not found" in text:
                                await print_warn(msg, f"Забанен в чате #{counter} {past_link}", have_logs)
                                should_continue = True
                                tried_accounts = 1
                                if past_link not in forbidden_links:
                                    with open(("app/analytics/forbidden_links.txt"), "a") as file:
                                        file.write(f"\n{past_link}")
                                    forbidden_links.append(past_link)
                                break
                            elif "unregistered" in text:
                                await print_error(msg, "АККАУНТ ВЫЛЕТЕЛ", have_logs)
                                await deleting_account(
                                    client=client,
                                    clients=new_clients,
                                    old_clients=old_clients,
                                    session_maker=session_maker
                                )
                                first_length -= 1
                                delay = ceil(delay / first_length)
                                break
                            else:
                                print(e)
                                await print_error(msg, f"Ошибка при вступлении в #{counter} {past_link}", have_logs)
                            if past_link not in invalid_links:
                                with open("app/analytics/invalid_links.txt", "a") as file:
                                    file.write(f"\n{past_link}")
                                invalid_links.append(past_link)
                            await asyncio.sleep(for_sleep)
                            tried_accounts = 1
                            should_continue = True
                            break
                        finally:
                            await asyncio.sleep(choice([1, 1.2, 1.4]))
                    if should_continue:
                        if not was_delayed:
                            new_clients.remove(client)
                            asyncio.gather(
                                account_waiting(
                                    client, abs(delay - 2), new_clients
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
                                    client: Client = choice(new_clients)
                                    try:
                                        chat = await client.join_chat(chat.id)
                                    except UserAlreadyParticipant:
                                        chat = await client.get_chat(chat.id)
                                    except Exception:
                                        break
                                    await asyncio.sleep(choice([1, 1.2, 1.4]))
                                    await print_info(client.name)
                                try:
                                    await sending(
                                        client=client,
                                        message=message,
                                        chat=chat,
                                        reply_id=thread_id,
                                    )
                                    await print_info(msg, f"Отправил в чат #{counter} {past_link}", have_logs)
                                    was_sent += 1
                                    if past_link not in valid_links:
                                        with open("app/analytics/valid_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        valid_links.append(past_link)
                                    break
                                except ChatWriteForbidden:
                                    await print_warn(msg, f"Забанен в #{counter} {past_link}", have_logs)
                                    if past_link not in forbidden_links:
                                        with open("app/analytics/forbidden_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        forbidden_links.append(past_link)
                                    should_continue = True
                                    break
                                except BadRequest as e:
                                    text = str(e).lower()
                                    if "spam" in text:
                                        await print_warn(msg, f"{client.name} дали спам. Пишу @SpamBot", have_logs)
                                        await asyncio.sleep(0.5)
                                        await client.send_message(
                                            chat_id="SpamBot", text="/start"
                                        )
                                        await print_info(msg, "Успешно снял спам", have_logs)
                                        if past_link not in valid_links:
                                            with open("app/analytics/valid_links.txt", "a") as file:
                                                file.write(f"\n{past_link}")
                                            valid_links.append(past_link)
                                        if tried_accounts > 3:
                                            await print_error(msg, "Ошибка в аккаунте", have_logs)
                                            new_clients.remove(client)
                                            again = True
                                        continue
                                    elif "closed" in text:
                                        await print_warn(msg, f"Тема закрыта #{counter} {past_link}", have_logs)
                                        should_continue = True
                                        if past_link not in closed_topic_links:
                                            with open("app/analytics/closed_topic_links.txt", "a") as file:
                                                file.write(f"\n{past_link}")
                                            closed_topic_links.append(past_link)
                                        if past_link not in invalid_links:
                                            with open("app/analytics/invalid_links.txt", "a") as file:
                                                file.write(f"\n{past_link}")
                                            invalid_links.append(past_link)
                                    elif 'required' in text:
                                        await print_warn(msg, f"Запрещено писать #{counter} {past_link}", have_logs)
                                        if past_link not in invalid_links:
                                            with open(msg, "app/analytics/invalid_links.txt", "a") as file:
                                                file.write(f"\n{past_link}")
                                            invalid_links.append(past_link)
                                    else:
                                        await print_warn(msg, f'Ошибка при отправке {e}', have_logs)
                                    break
                                except (SlowmodeWait, SlowmodeWaitFlood) as e:
                                    await print_info( msg, f"Отправлю через {e.value} #{counter} {past_link}", have_logs)
                                    was_sent += 1
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
                                    await print_warn(msg, "Дали спам. Пишу @SpamBot", have_logs)
                                    await asyncio.sleep(0.5)
                                    await client.send_message(chat_id="SpamBot", text="/start")
                                    await print_info(msg, "Успешно снял спам", have_logs)
                                    if past_link not in valid_links:
                                        with open("app/analytics/valid_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        valid_links.append(past_link)
                                    if tried_accounts > 3:
                                        await print_error(msg, "Ошибка в аккаунте", have_logs)
                                        new_clients.remove(client)
                                        again = True
                                    await asyncio.sleep(choice([0.5, 0.6, 0.7]))
                                    continue
                                except FloodWait as e:
                                    await print_warn(msg, f"Жду {e.value} секунд", have_logs)
                                    if past_link not in valid_links:
                                        with open("app/analytics/valid_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        valid_links.append(past_link)
                                    new_clients.remove(client)
                                    asyncio.gather(
                                        account_waiting(client, e.value, new_clients)
                                    )
                                    break
                                except Exception as e:
                                    text: str = str(e).lower()
                                    if "private" in text:
                                        await print_warn(msg, f"Чат приватный #{counter} {past_link}", have_logs)
                                    elif "payment" in text:
                                        await print_warn(msg, f"Запрещено писать #{counter} {past_link}", have_logs)
                                    elif "forbidden" in text:
                                        await print_warn(msg, f"Забанен в чате #{counter} {past_link}", have_logs)
                                        if past_link not in forbidden_links:
                                            with open("app/analytics/forbidden_links.txt", "a") as file:
                                                file.write(f"\n{past_link}")
                                            forbidden_links.append(past_link)
                                        break
                                    else:
                                        print(e)
                                        await print_error(msg, f"Ошибка при отправке в #{counter} {past_link}", have_logs)
                                    should_continue = True
                                    if past_link not in invalid_links:
                                        with open("app/analytics/invalid_links.txt", "a") as file:
                                            file.write(f"\n{past_link}")
                                        invalid_links.append(past_link)
                                    break
                        if not has_message:
                            await print_error(msg, 'НЕТ ОФФЕРА', have_logs)
                            try:
                                new_clients.remove(client)
                            except Exception:
                                pass
                            first_length -= 1
                            delay = ceil(delay / first_length)
                    else:
                        await print_warn(msg, f"Не удалось получить чат {past_link}", have_logs)
                    if client in new_clients:
                        new_clients.remove(client)
                        asyncio.gather(
                            account_waiting(client, (delay - 4), new_clients)
                        )
                    if should_continue:
                        await asyncio.sleep(for_sleep)
                        continue
                    if choice([True, False]):
                        asyncio.gather(chat_leaving(client, chat, choice([5, 10, 20])))
                        await print_info(msg, f'Вышел из чата #{counter}', have_logs)
                    await asyncio.sleep(for_sleep)
                else:
                    await print_info(msg, f"Уже отправил в чат {link}", have_logs)
        with open((f"app/database/groups/used_links{telegram_id}.txt"), "w") as file:
            file.write("")
        await print_info(msg, f'Рассылка завершена. Отправлено в #{sent} чатов', have_logs)
        removed = sent - was_sent
        if from_zalp:
            await msg.answer(
                text=i18n.text.user.summarize(
                    name=msg.from_user.first_name,
                    sent=sent,
                    removed=removed,
                    stayed=was_sent,
                    removed_persent=(removed/sent)*100,
                    stayed_persent=(was_sent/sent)*100
                ),
                reply_markup=get_workpulse_kbd(i18n=i18n, have_up=False, down='zalp_done')
            )
    except CancelledError:
        await print_info(msg, "Команда отменена", have_logs)
    except Exception as e:
        print(e)
        await print_error(msg, f"Ошибка при выполнении рассылки по группам: {e}", have_logs)
        removed = sent - was_sent
        if from_zalp:
            await msg.answer(
                text=i18n.text.user.summarize(
                    name=msg.from_user.first_name,
                    sent=sent,
                    removed=removed,
                    stayed=was_sent,
                    removed_persent=(removed/sent)*100,
                    stayed_persent=(was_sent/sent)*100
                ),
                reply_markup=get_workpulse_kbd(i18n=i18n, have_up=False, down='zalp_done')
            )

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
            with open("app/analytics/valid_links.txt", "a") as file:
                file.write(f"\n{past_link}")
            valid_links.append(past_link)
    except Exception:
        if past_link not in invalid_links:
            with open("app/analytics/invalid_links.txt", "a") as file:
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