import asyncio
import os

from redis import Redis
from pyrogram import Client
from aiogram import Bot, F, Router
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, FSInputFile)
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.settings import add_client
from bot.states import AdminMainSG
from bot.utils import format_database, process_users_mailing, format_accounts_db
from bot.keyboards import (
    get_yes_no_kbd, get_accepted_kbd, get_declined_kbd,
    get_startpanel_kbd, get_back_kbd, get_accounts_kbd
)
from bot.database.requests import get_all_users, delete_account

admin_router = Router()

@admin_router.message(CommandStart())
@admin_router.callback_query(F.data == 'back_admin_menu')
async def cmd_admin_start(obj: Message | CallbackQuery, i18n: TranslatorRunner) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if not isinstance(obj, Message):
        await obj.message.delete()
    await msg.answer(
        text=i18n.text.admin.start(),
        reply_markup=get_startpanel_kbd(i18n=i18n)
    )

@admin_router.callback_query(F.data == 'accounts')
@admin_router.callback_query(F.data == 'back_accounts')
async def cmd_admin_accounts(call: CallbackQuery, i18n: TranslatorRunner, clients: list[Client], rstorage: Redis, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await format_accounts_db(session_maker=session_maker)
    for client in clients:
        await rstorage.set(client.phone_number, 0)
    await call.message.answer_document(
        document=FSInputFile(path='bot/media/accounts_database.txt'),
        caption=i18n.text.admin.accounts(),
        reply_markup=await get_accounts_kbd(i18n=i18n, clients=clients, rstorage=rstorage)
    )

@admin_router.callback_query(F.data.startswith('+'))
async def cmd_choose_acc(call: CallbackQuery, i18n: TranslatorRunner, clients: list[Client], rstorage: Redis) -> None:
    data: str = call.data
    to_set: int = 1 if int(await rstorage.get(data)) == 0 else 0
    await rstorage.set(data, to_set)
    await call.message.edit_reply_markup(reply_markup=await get_accounts_kbd(i18n=i18n, clients=clients, rstorage=rstorage))

@admin_router.callback_query(F.data == 'delete_accs')
async def cmd_delete_accs(call: CallbackQuery, i18n: TranslatorRunner, clients: list[Client], rstorage: Redis) -> None:
    data: dict[str: bool] = {}
    for client in clients:
        data[client.phone_number] = True if int(await rstorage.get(client.phone_number)) == 1 else False
    accounts = [client for client, to_delete in data.items() if to_delete]
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.admin.delete_accs(accounts='\n'.join(accounts)),
        reply_markup=get_yes_no_kbd(i18n=i18n, on_yes='sure_delete_accs', on_no='back_accounts')
    )

@admin_router.callback_query(F.data == 'sure_delete_accs')
async def cmd_sure_delete_accs(call: CallbackQuery, i18n: TranslatorRunner, clients: list[Client], rstorage: Redis, session_maker: async_sessionmaker) -> None:
    for client in clients:
        if int(await rstorage.get(client.phone_number)):
            clients.remove(client)
            await delete_account(session_maker=session_maker, phone=client.phone_number)
            await client.stop()
            await asyncio.sleep(0.5)
            os.remove(path=f'sessions/{client.phone_number[1:]}.session')
    await call.message.edit_text(
        text=i18n.text.admin.accounts_deleted(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )

@admin_router.callback_query(F.data == 'receive_code')
async def cmd_receive_code(call: CallbackQuery, i18n: TranslatorRunner, clients: list[Client], rstorage: Redis) -> None:
    code: str
    client: Client
    for cli in clients:
        if int(await rstorage.get(cli.phone_number)):
            client = cli
            break
    async for message in client.get_chat_history(chat_id=777000, limit=1):
        code = (message.text).split('.')[0].split(':')[-1][1:]
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.admin.receive_code(phone=client.phone_number, code=code),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )

@admin_router.callback_query(F.data == 'add_accs')
async def cmd_admin_add_accs(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.admin.enter_phone(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    await state.set_state(AdminMainSG.phone)

@admin_router.message(StateFilter(AdminMainSG.phone))
async def cmd_admin_enter_api_id(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_api_id(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    await rstorage.set(msg.from_user.id, f'phone:{msg.text};')
    await state.set_state(AdminMainSG.api_id)

@admin_router.message(StateFilter(AdminMainSG.api_id))
async def cmd_admin_enter_api_hash(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_api_hash(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'api_id:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.api_hash)

@admin_router.message(StateFilter(AdminMainSG.api_hash))
async def cmd_admin_enter_app_version(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_app_version(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'api_hash:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.app_version)

@admin_router.message(StateFilter(AdminMainSG.app_version))
async def cmd_admin_enter_device_model(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_device_model(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'app_version:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.device_model)

@admin_router.message(StateFilter(AdminMainSG.device_model))
async def cmd_admin_enter_system_version(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_system_version(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'device_model:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.system_version)

@admin_router.message(StateFilter(AdminMainSG.system_version))
async def cmd_admin_enter_lang_code(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_lang_code(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'system_version:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.lang_code)

@admin_router.message(StateFilter(AdminMainSG.lang_code))
async def cmd_admin_enter_password(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_password(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'lang_code:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.password)

@admin_router.message(StateFilter(AdminMainSG.password))
async def cmd_admin_enter_proxy_scheme(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_proxy_scheme(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'password:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.proxy_scheme)

@admin_router.message(StateFilter(AdminMainSG.proxy_scheme))
async def cmd_admin_enter_proxy_host(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_proxy_host(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'proxy_scheme:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.proxy_host)

@admin_router.message(StateFilter(AdminMainSG.proxy_host))
async def cmd_admin_enter_proxy_port(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_proxy_port(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'proxy_hostname:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.proxy_port)

@admin_router.message(StateFilter(AdminMainSG.proxy_port))
async def cmd_admin_enter_proxy_username(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_proxy_username(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'proxy_port:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.proxy_username)

@admin_router.message(StateFilter(AdminMainSG.proxy_username))
async def cmd_admin_enter_proxy_password(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis) -> None:
    await msg.answer(
        text=i18n.text.admin.enter_proxy_password(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    value: str = await rstorage.get(name=msg.from_user.id) + f'proxy_username:{msg.text};'
    await rstorage.set(name=msg.from_user.id, value=value)
    await state.set_state(AdminMainSG.proxy_password)

@admin_router.message(StateFilter(AdminMainSG.proxy_password))
async def cmd_admin_enter_code(msg: Message, i18n: TranslatorRunner, state: FSMContext, clients: list[Client], rstorage: Redis, session_maker: async_sessionmaker) -> None:
    to_start: dict = {}
    await msg.answer(
        text=i18n.text.admin.enter_code(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    data: str = await rstorage.get(name=msg.from_user.id) + f'proxy_password:{msg.text}'
    to_start = {part.split(':')[0]: part.split(':')[1] for part in data.split(';')}
    try:
        await state.set_state(AdminMainSG.enter_code)
        await rstorage.delete('code')
        await add_client(data=to_start, rstorage=rstorage, session_maker=session_maker, clients=clients)
    except Exception as e:
        print(e)
        await msg.answer(
            text=i18n.text.admin.account_failed(),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
        )

@admin_router.message(StateFilter(AdminMainSG.enter_code))
async def cmd_admin_account_done(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    await rstorage.set('code', int(msg.text))
    await msg.answer(
        text=i18n.text.admin.account_added(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_accounts')
    )
    await rstorage.delete(msg.from_user.id)
    await state.clear()

@admin_router.callback_query(F.data == 'mailing')
async def cmd_admin_mailing(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    await call.message.edit_text(
        text=i18n.text.admin.mailing(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_admin_menu')
    )
    await state.set_state(AdminMainSG.mailing)

@admin_router.message(StateFilter(AdminMainSG.mailing))
async def cmd_process_mailing(msg: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot, session_maker: async_sessionmaker[AsyncSession]) -> None:
    users: list[dict] = await get_all_users(session_maker=session_maker)
    ides: list[int] = [u['telegram_id'] for u in users]
    asyncio.gather(process_users_mailing(bot=bot, msg=msg, ides=ides))
    await msg.answer(
        text=i18n.text.admin.mailing_done(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_admin_menu')
    )
    await state.clear()

@admin_router.callback_query(F.data == 'database')
async def cmd_admin_database(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker[AsyncSession]) -> None:
    await call.message.delete()
    await format_database(session_maker=session_maker)
    await call.message.answer_document(
        document=FSInputFile('bot/media/database.txt'),
        caption=i18n.text.admin.database(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_admin_menu')
    )

@admin_router.callback_query(F.data.startswith('decline'))
@admin_router.callback_query(F.data.startswith('call'))
@admin_router.callback_query(F.data.startswith('watcher'))
async def cmd_verify(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    data: str = call.data.split('_')
    cmd: str = data[0].replace('_', '')
    meta: str = data[-1]
    to_answer: str = ''
    reply_markup: InlineKeyboardMarkup
    if cmd == 'decline':
        to_answer = i18n.text.admin.decline()
        reply_markup=get_yes_no_kbd(i18n=i18n, on_yes=f'suredec_{meta}', on_no='deletemsg')
    elif cmd == 'call':
        to_answer = i18n.text.admin.call()
        reply_markup=get_yes_no_kbd(i18n=i18n, on_yes=f'surecall_{meta}', on_no='deletemsg')
    else:
        to_answer = i18n.text.admin.watcher()
        reply_markup=get_yes_no_kbd(i18n=i18n, on_yes=f'surewatch_{meta}', on_no='deletemsg')
    await call.message.answer(
        text=to_answer,
        reply_markup=reply_markup
    )
    await state.set_state(AdminMainSG.verifying)

@admin_router.callback_query(F.data.startswith('suredec_'))
async def cmd_suredec(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot) -> None:
    data: str = call.data.split('_')
    meta: str = data[-1].split('.')
    ide: int = int(meta[0])
    branch: str = meta[1]
    anti_branch: str = '🔴 Standard' if branch == 'fastlane' else '🔰 Fastlane'
    for_callback: str = 'back_standard' if branch == 'fastlane' else 'back_fastlane'
    name: str = meta[-1]
    await bot.send_photo(
        chat_id=ide,
        photo='https://t.me/sksjkdksnsjdjdndksm/3',
        caption=i18n.text.user.declined(
            niche=branch.capitalize(),
            name=name,
            anti_niche=anti_branch
        ),
        reply_markup=get_declined_kbd(i18n=i18n, other_text=anti_branch, other_call=for_callback)
    )
    await call.message.edit_text(text=i18n.text.done())
    await state.clear()
    await asyncio.sleep(2)
    await call.message.delete()

@admin_router.callback_query(F.data.startswith('surecall_'))
async def cmd_surecall(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, bot: Bot) -> None:
    data: str = call.data.split('_')
    meta: str = data[-1].split('.')
    ide: int = int(meta[0])
    name: str = meta[-1]
    await bot.send_photo(
        chat_id=ide,
        photo='https://t.me/sksjkdksnsjdjdndksm/5',
        caption=i18n.text.user.accepted(name=name),
        reply_markup=get_accepted_kbd(i18n=i18n)
    )
    await call.message.edit_text(text=i18n.text.done())
    await state.clear()
    await asyncio.sleep(2)
    await call.message.delete()

@admin_router.callback_query(F.data == 'deletemsg')
async def cmd_delete(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.delete()