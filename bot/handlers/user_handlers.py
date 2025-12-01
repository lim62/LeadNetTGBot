import asyncio
import os

from redis import Redis
from pyrogram import Client
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.config import Config
from bot.states import UserMainSG
from bot.database.requests import upsert_user, get_all_users
from bot.keyboards import (
    get_start_kbd, get_back_kbd, get_verif_kbd, 
    get_fastlane_kbd, get_delta_kbd, get_send_kbd,
    get_success_kbd, get_standard_kbd, get_time_kbd,
    get_leadpanel_kbd, get_pulse_kbd, get_tarif_kbd,
    get_workpulse_kbd, get_offer_kdb, get_zalp_kbd,
    give_chats_kbd, get_end_kbd, get_yes_no_kbd
)
from bot.utils import change_photo
from app.services.groups import process_async_groups

user_router = Router()

tasks: dict[int, asyncio.Task] = {}

@user_router.message(CommandStart())
@user_router.callback_query(F.data == 'back_start')
async def cmd_start(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    from_ref: bool = False
    msg = obj if isinstance(obj, Message) else obj.message
    first_name: str = obj.from_user.first_name
    if isinstance(obj, Message):
        args = msg.text.split()
        payload = args[1] if len(args) > 1 else None
        user = await get_all_users(session_maker=session_maker, telegram_id=obj.from_user.id)
        if not user and payload:
            msg = await msg.answer(text=i18n.text.user.start_stage1_menu())
            await asyncio.sleep(2)
            referal = await get_all_users(session_maker=session_maker, telegram_id=int(payload))
            await upsert_user(
                session_maker=session_maker,
                telegram_id=int(payload),
                credit=int(referal[0]['credit']) + 5
            )
            from_ref = True
        else:   
            msg = await msg.answer(text=i18n.text.user.start_stage1())
            await asyncio.sleep(2)
        await msg.delete()
        msg = await msg.answer(text=i18n.text.user.start_stage2())
        await asyncio.sleep(2)
        await msg.delete()
        msg = await msg.answer(text=i18n.text.user.start_stage3())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_video(
        video='https://t.me/sksjkdksnsjdjdndksm/10',
        caption=i18n.text.user.menu(name=first_name),
        reply_markup=get_start_kbd(i18n=i18n)
    )
    await state.clear()
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        username=f'@{obj.from_user.username}',
        status='user',
        stage='menu',
        messages=30,
        credit=5,
        have_prepared=False,
        from_ref=from_ref
    )

@user_router.callback_query(F.data == 'pulse')
@user_router.callback_query(F.data == 'back_pulse')
async def cmd_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/26',
        caption=i18n.text.user.pulse(name=call.from_user.first_name),
        reply_markup=get_pulse_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'how_works_pulse')
async def cmd_how_works_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/30',
        caption=i18n.text.user.how_works_pulse(),
        reply_markup=get_workpulse_kbd(i18n=i18n, down='tg_chats', have_up=False)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='how_works_pulse'
    )

@user_router.callback_query(F.data == 'tg_chats')
async def cmd_tg_chats(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/24',
        caption=i18n.text.user.tg_chats(),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='how_works_pulse', down='work_in_place')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='tg_chats'
    )

@user_router.callback_query(F.data == 'work_in_place')
async def cmd_work_in_place(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/31',
        caption=i18n.text.user.work_in_place(),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='tg_chats', down='offer_pulse')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='work_in_place'
    )

@user_router.callback_query(F.data == 'offer_pulse')
async def cmd_offer_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/32',
        caption=i18n.text.user.offer_pulse(),
        reply_markup=get_offer_kdb(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='offer_pulse'
    )

@user_router.callback_query(F.data == 'examples_offer')
async def cmd_examples_offer(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.user.need_status(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='offer_pulse', have_down=False)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='examples_offer'
    )

@user_router.callback_query(F.data == 'test_zalp')
async def cmd_test_zalp(call: CallbackQuery, i18n: TranslatorRunner, bot: Bot, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    user_id: int = call.from_user.id
    photos = await bot.get_user_profile_photos(call.from_user.id)
    if photos.total_count == 0:
        await call.message.answer_photo(
            photo=FSInputFile(path='bot/media/avatars/draft.jpg'),
            caption=i18n.text.user.start_zalp(name=call.from_user.first_name),
        )
        return
    photo = photos.photos[0][-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"bot/media/avatars/{user_id}.jpg")
    change_photo(user_photo_path=f"bot/media/avatars/{user_id}.jpg", user_id=user_id)
    await call.message.answer_photo(
        photo=FSInputFile(path=f'bot/media/avatars/pusk_prepare{user_id}.png'),
        caption=i18n.text.user.test_zalp(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='offer_pulse', down='give_chats', down_text=i18n.btn.yes_go(), have_back=False)
    )
    os.remove(f"bot/media/avatars/{user_id}.jpg")
    os.remove(f'bot/media/avatars/pusk_prepare{user_id}.png')
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='test_zalp'
    )

@user_router.callback_query(F.data == 'give_chats')
@user_router.callback_query(F.data == 'back_give_chats')
async def cmd_give_chats(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    msg = call.message
    if call.data == 'give_chats':
        await call.message.delete()
        msg = await call.message.answer(text=i18n.text.user.system())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/33',
        caption=i18n.text.user.give_chats(name=call.from_user.first_name, ref_link=f'https://t.me/Lead_Net_Bot?start={call.from_user.id}'),
        reply_markup=give_chats_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='give_chats'
    )

@user_router.callback_query(F.data == 'upload_chats')
async def cmd_upload_chats(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/34',
        caption=i18n.text.user.upload_chats(),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='back_give_chats', have_down=False, have_back=False)
    )
    await state.set_state(UserMainSG.load_chats)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='upload_chats'
    )

@user_router.message(StateFilter(UserMainSG.load_chats))
@user_router.callback_query(F.data == 'start_zalp')
async def cmd_start_zalp(obj: Message | CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    links: list[str] = []
    msg = obj if isinstance(obj, Message) else obj.message
    if not isinstance(obj, Message):
        await obj.message.delete()
    else:
        links = [link.strip() for link in msg.text.split('\n') if link.startswith('http')] + [f'https://{link.strip()}' for link in msg.text.split('\n') if link.startswith('t.me')]
        if not links:
            await msg.answer(
                text=i18n.text.user.no_links()
            )
            return
        elif len(links) > 10:
            await msg.answer(
                text=i18n.text.user.much_links()
            )
            return
    links += ["https://t.me/salespractice","https://t.me/toppiar_chat","https://t.me/spb_cs","https://t.me/mskcpro","https://t.me/clubbusinessist","https://t.me/mary_vvvverh","https://t.me/+fvl0RYvNDh9jN2Ri","https://t.me/biznesfamily_n1","https://t.me/startupschoolsk","https://t.me/tclubnetwork","https://t.me/kosmetologytop","https://t.me/+R_KxUQG5hYo5ZjAy","https://t.me/filigrad_all","https://t.me/+OY1QSBoSt_NhMTJi","https://t.me/+hVFpPc7sFXA2MTQy","https://t.me/+1XT7FX00zGlmNjE0","http://t.me/+RtHbcvNmgfYwZWI6","https://t.me/+20m4ulAwHQVkMmQy","https://t.me/+YSepHSsKfN82Yzk6","https://t.me/+qd5P1QZJnVVjOGIy"]
    with open((f'app/database/groups/links{obj.from_user.id}.txt'), 'w') as file:
        file.write('\n'.join(links))
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/41',
        caption=i18n.text.user.start_zalp(name=obj.from_user.first_name),
        reply_markup=get_zalp_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='start_zalp'
    )

@user_router.callback_query(F.data == 'show_offer')
async def cmd_show_offer(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    have_prepared: dict = (await get_all_users(session_maker=session_maker, telegram_id=call.from_user.id))[0]['have_prepared']
    down: str = 'zalp_done' if have_prepared else 'starting'
    await call.message.delete()
    await call.message.answer_video(
        video='https://t.me/sksjkdksnsjdjdndksm/42',
        caption=i18n.text.user.show_offer(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, up='start_zalp', down=down)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='show_offer'
    )

@user_router.callback_query(F.data == 'starting')
async def cmd_starting(call: CallbackQuery, i18n: TranslatorRunner, clients: dict[Client, int], rstorage: Redis, session_maker: async_sessionmaker) -> None:
    our_clients: list[Client] = [client for client, owner in clients.items() if owner == 0]
    for client in our_clients:
        client: Client
        await client.send_video(
            chat_id='me',
            video='https://t.me/sksjkdksnsjdjdndksm/42',
            caption=i18n.text.user.zalp_mail(ref_link=f'https://t.me/Lead_Net_Bot?start={call.from_user.id}')
        )
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.user.mailing_process(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse')
    )
    with open((f"app/database/groups/used_links{call.from_user.id}.txt"), "w") as file:
        file.write(' ')
    asyncio.ensure_future(
        process_async_groups(
            old_clients=clients,
            msg=call.message,
            telegram_id=call.from_user.id,
            i18n=i18n,
            rstorage=rstorage,
            session_maker=session_maker,
            MESSAGE_DELAY=1,
            have_logs=False,
            for_all=False,
            from_zalp=True
        )
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        have_prepared=True
    )

@user_router.callback_query(F.data == 'zalp_done')
@user_router.callback_query(F.data == 'back_zalp_done')
async def cmd_zalp_done(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    msg = call.message
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/36',
        caption=i18n.text.user.zalp_done(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, down='continue_prepare', down_text=i18n.btn.continue_prepare(), have_up=False)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='zalp_done'
    )

@user_router.callback_query(F.data == 'continue_prepare')
async def cmd_continue_prepare(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/37',
        caption=i18n.text.user.after_impulse(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, down='show_nativ', up='back_zalp_done')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='continue_prepare'
    )

@user_router.callback_query(F.data == 'show_nativ')
async def cmd_show_nativ(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/38',
        caption=i18n.text.user.show_nativ(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, down='nativ_sent', up='continue_prepare', down_text=i18n.btn.zalp())
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='show_nativ'
    )

@user_router.callback_query(F.data == 'nativ_sent')
async def cmd_nativ_sent(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/40',
        caption=i18n.text.user.nativ_sent(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, down='try_stories', have_up=False)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='nativ_sent'
    )

@user_router.callback_query(F.data == 'try_stories')
async def cmd_try_stories(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/39',
        caption=i18n.text.user.try_stories(name=call.from_user.first_name),
        reply_markup=get_workpulse_kbd(i18n=i18n, have_up=False, down='end_prepare')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='try_stories'
    )
    
@user_router.callback_query(F.data == 'end_prepare')
async def cmd_end_prepare(call: CallbackQuery, i18n: TranslatorRunner) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/44',
        caption=i18n.text.user.end_prepare(name=call.from_user.first_name),
        reply_markup=get_end_kbd(i18n=i18n)
    )

@user_router.callback_query(F.data == 'constructor')
@user_router.callback_query(F.data == 'back_constructor')
async def cmd_constructor(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    status = (await get_all_users(session_maker=session_maker, telegram_id=call.from_user.id))[0]['status']
    if status and status != 'user':
        pass
    else:
        await call.message.delete()
        await call.message.answer(
            text=i18n.text.user.need_status(name=call.from_user.first_name),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse')
        )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='constructor'
    )

@user_router.callback_query(F.data == 'start_pulse')
@user_router.callback_query(F.data == 'back_start_pulse')
async def cmd_start_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker, state: FSMContext) -> None:
    status = (await get_all_users(session_maker=session_maker, telegram_id=call.from_user.id))[0]['status']
    await call.message.delete()
    if status and status != 'user':
        await call.message.answer(
            text=i18n.text.user.ask_offer(),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse')
        )
        await state.set_state(UserMainSG.load_offer)
    else:
        await call.message.answer(
            text=i18n.text.user.need_status(name=call.from_user.first_name),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse')
        )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='start_pulse'
    )

@user_router.message(StateFilter(UserMainSG.load_offer))
async def cmd_offer_clients(msg: Message, i18n: TranslatorRunner, rstorage: Redis, state: FSMContext, clients: dict[Client, int]) -> None:
    our_clients: list[Client] = [client for client, owner in clients.items() if owner == msg.from_user.id]
    for client in our_clients:
        client: Client
        value = await rstorage.get(client.phone_number)
        if value and int(value):
            if msg.media_group_id:
                await msg.answer(
                    text=i18n.text.admin.no_media_groups(),
                    reply_markup=get_back_kbd(i18n=i18n, callback_data='soft')
                )
                return
            elif getattr(msg, "photo", None):
                media = msg.photo.file_id
                await client.send_photo(chat_id='me', photo=media, caption=msg.caption, caption_entities=msg.caption_entities)
            elif getattr(msg, "video", None):
                media = msg.video.file_id
                await client.send_video(chat_id='me', video=media, caption=msg.caption, caption_entities=msg.caption_entities)
            else:
                await client.send_message(chat_id='me', text=msg.text, entities=msg.entities)
    await msg.answer(
        text=i18n.text.user.ask_chats(),
        reply_markup=get_workpulse_kbd(
            i18n=i18n,
            have_up=False,
            down='start_paid_mailing',
            down_text=i18n.btn.contin(),
            back='back_pulse'
        )
    )
    await state.set_state(UserMainSG.load_chats)

@user_router.callback_query(F.data == 'start_paid_mailing')
@user_router.message(StateFilter(UserMainSG.load_chats))
async def cmd_chats_clients(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    msg: Message = obj if isinstance(obj, Message) else obj.message
    path: str = f'app/database/groups/links{obj.from_user.id}.txt'
    links: list[str] = []
    if isinstance(obj, CallbackQuery):
        await obj.message.delete()
    if isinstance(obj, Message):
        if not os.path.exists(path):
            with open('app/database/groups/links.txt', 'r') as file:
                links = [link.strip() for link in file.readlines() if link.startswith('http')] + [f'https://{link.strip()}' for link in file.readlines() if link.startswith('t.me')] 
            with open(path, 'w') as file:
                file.write('\n'.join(links))
        links = [link.strip() for link in msg.text.split('\n') if link.startswith('http')] + [f'https://{link.strip()}' for link in msg.text.split('\n') if link.startswith('t.me')] 
        with open(path, 'a') as file:
            file.write('\n'.join(links))
    await msg.answer(
        text=i18n.text.user.sure_start(),
        reply_markup=get_yes_no_kbd(i18n=i18n, on_yes='sure_paid_mailing', on_no='back_pulse')
    )

@user_router.callback_query(F.data == 'sure_paid_mailing')
async def cmd_start_(call: CallbackQuery, i18n: TranslatorRunner, rstorage: Redis, session_maker: async_sessionmaker, clients: dict[Client, int]) -> None:
    our_clients: list[Client] = [client for client, owner in clients.items() if owner == call.from_user.id]
    task: asyncio.Task | None = None
    try:
        task = tasks[call.from_user.id]
    except Exception: 
        pass
    if task:
        task.cancel()
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.admin.start_groups(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse')
    )
    task = asyncio.ensure_future(
        process_async_groups(
            old_clients=our_clients,
            msg=call.message,
            telegram_id=call.from_user.id,
            i18n=i18n,
            rstorage=rstorage,
            session_maker=session_maker,
            MESSAGE_DELAY=1500,
            have_logs=False,
            for_all=False,
            from_zalp=False
        )
    )
    tasks[call.from_user.id] = task

@user_router.callback_query(F.data == 'tarifs')
@user_router.callback_query(F.data == 'back_tarifs')
async def cmd_tarifs(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/43',
        caption=i18n.text.user.tarifs(name=call.from_user.first_name),
        reply_markup=get_tarif_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='tarifs'
    )

@user_router.callback_query(F.data == 'pulse_testum')
async def cmd_pulse_testum(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/45',
        caption=i18n.text.user.pulse_testum(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs', text=i18n.btn.true_back())
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse_testum'
    )

@user_router.callback_query(F.data == 'pulse_base')
async def cmd_pulse_base(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/46',
        caption=i18n.text.user.pulse_base(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs', text=i18n.btn.true_back())
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse_base'
    )

@user_router.callback_query(F.data == 'pulse_pro')
async def cmd_pulse_pro(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/47',
        caption=i18n.text.user.pulse_pro(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs', text=i18n.btn.true_back())
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse_pro'
    )

@user_router.callback_query(F.data == 'pulse_ultra')
async def cmd_pulse_ultra(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/48',
        caption=i18n.text.user.pulse_ultra(),
        reply_markup=get_workpulse_kbd(i18n=i18n, have_up=False, down='standard', down_text=i18n.btn.verification(), back_text=i18n.btn.true_back(), back='back_tarifs')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse_ultra'
    )

@user_router.callback_query(F.data == 'profile')
@user_router.callback_query(F.data == 'back_profile')
async def cmd_profile(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    data: dict = (await get_all_users(session_maker=session_maker, telegram_id=call.from_user.id))[0]
    status: str = data['status']
    credit: int = data['credit']
    status = f'💸 {status.upper()}' if status != 'user' else '🫰 USER'
    credit = int(credit) if credit else 0
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/28',
        caption=i18n.text.user.profile(
            name=call.from_user.first_name,
            status=status,
            expired='0',
            credit=credit,
            messages='0',
            ref_link=f'https://t.me/Lead_Net_Bot?start={call.from_user.id}'
        ),
        reply_markup=get_workpulse_kbd(i18n=i18n, have_up=False, down='start_pulse', down_text=i18n.btn.skyrocket()),
        link_preview_options=False
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='profile'
    )

@user_router.callback_query(F.data == 'verification')
@user_router.callback_query(F.data == 'back_verif')
async def cmd_verification(call: CallbackQuery, i18n: TranslatorRunner, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    try:
        await rstorage.delete(call.from_user.id)
    except Exception:
        pass
    if call.data == 'verification':
        await call.message.delete()
        msg = await call.message.answer(text=i18n.text.user.verif_stage1())
        await asyncio.sleep(2)
        msg = await msg.edit_text(text=i18n.text.user.verif_stage2())
        await asyncio.sleep(2)
    else:
        msg = call.message
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/11',
        caption=i18n.text.user.verification(name=call.from_user.first_name),
        reply_markup=get_verif_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='verification'
    )

@user_router.callback_query(F.data == 'fastlane')
@user_router.callback_query(F.data == 'back_fastlane')
async def cmd_fastlane(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    await rstorage.delete(call.from_user.id)
    if call.data == 'fastlane':
        await call.message.delete()
        msg = await call.message.answer(text=i18n.text.user.fastlane_stage1())
        await asyncio.sleep(2)
        msg = await msg.edit_text(text=i18n.text.user.fastlane_stage2())
        await asyncio.sleep(2)
    else:
        msg = call.message
    await msg.delete()
    await msg.answer_video(
        video='https://t.me/sksjkdksnsjdjdndksm/12',
        caption=i18n.text.user.fastlane(name=call.from_user.first_name),
        reply_markup=get_fastlane_kbd(i18n=i18n)
    )
    await state.set_state(UserMainSG.fastlane)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='fastlane'
    )

@user_router.callback_query(F.data == 'delta')
async def cmd_delta(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/13',
        caption=i18n.text.user.delta(name=call.from_user.first_name),
        reply_markup=get_delta_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='delta'
    )

@user_router.message(StateFilter(UserMainSG.fastlane))
async def check_fastlane(msg: Message, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    product = msg.text
    if len(product) < 20:
        await msg.answer(text=i18n.text.user.no_traffic_stage1())
        return
    await rstorage.set(name=msg.from_user.id, value=f'fastlane:{product};')
    msg = await msg.answer(text=i18n.text.user.fastlane_send1())
    await asyncio.sleep(2)
    await msg.delete()
    msg = await msg.answer(text=i18n.text.user.fastlane_send2())
    await asyncio.sleep(2)
    await msg.delete()
    await msg.answer(
        text=i18n.text.user.fastlane_check(fastlane_product=product),
        reply_markup=get_send_kbd(i18n=i18n, send_data='send_fastlane', back_data='back_fastlane')
    )
    await state.clear()
    await upsert_user(
        session_maker=session_maker,
        telegram_id=msg.from_user.id,
        stage='send_fastlane'
    )

@user_router.callback_query(F.data == 'standard')
@user_router.callback_query(F.data == 'back_standard')
async def cmd_standard(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/14',
        caption=i18n.text.user.standard(name=call.from_user.first_name),
        reply_markup=get_standard_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='standard'
    )

@user_router.callback_query(F.data == 'product')
@user_router.callback_query(F.data == 'back_product')
async def cmd_product(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    if call.data == 'product':
        await call.message.delete()
        msg = await call.message.answer(text=i18n.text.user.product_stage1())
        await asyncio.sleep(2)
    else: 
        msg = call.message
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/15',
        caption=i18n.text.user.product(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_verif')
    )
    await state.set_state(UserMainSG.product)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='enter_product'
    )

@user_router.message(StateFilter(UserMainSG.product))
@user_router.callback_query(F.data == 'back_traffic')
async def input_product(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if isinstance(obj, Message):
        if len(msg.text) < 20:
            await msg.answer(text=i18n.text.user.no_traffic_stage1())
            return
        await rstorage.set(name=msg.from_user.id, value=f'product:{msg.text};')
        msg = await msg.answer(text=i18n.text.user.traffic_stage1())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/16',
        caption=i18n.text.user.sources_traffic(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_product')
    )
    await state.set_state(UserMainSG.sources_traffic)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='enter_traffic'
    )

@user_router.message(StateFilter(UserMainSG.sources_traffic))
@user_router.callback_query(F.data == 'back_model')
async def input_traffic(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if isinstance(obj, Message):
        if len(msg.text) < 20:
            await msg.answer(text=i18n.text.user.no_traffic_stage1())
            return
        value: str = await rstorage.get(name=msg.from_user.id) + f'traffic:{msg.text};'
        await rstorage.set(name=msg.from_user.id, value=value)
        msg = await msg.answer(text=i18n.text.user.model_stage1())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/17',
        caption=i18n.text.user.model(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_traffic')
    )
    await state.set_state(UserMainSG.model)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='enter_model'
    )

@user_router.message(StateFilter(UserMainSG.model))
@user_router.callback_query(F.data == 'back_economics')
async def input_model(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if isinstance(obj, Message):
        if len(msg.text) < 20:
            await msg.answer(text=i18n.text.user.no_traffic_stage1())
            return
        value: str = await rstorage.get(name=msg.from_user.id) + f'model:{msg.text};'
        await rstorage.set(name=msg.from_user.id, value=value)
        msg = await msg.answer(text=i18n.text.user.economics_stage1())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/18',
        caption=i18n.text.user.economics(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_model')
    )
    await state.set_state(UserMainSG.economics)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='enter_economics'
    )

@user_router.message(StateFilter(UserMainSG.economics))
@user_router.callback_query(F.data == 'back_time')
async def input_economics(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if isinstance(obj, Message):
        if len(msg.text) < 20:
            await msg.answer(text=i18n.text.user.no_traffic_stage1())
            return
        value: str = await rstorage.get(name=msg.from_user.id) + f'economics:{msg.text};'
        await rstorage.set(name=msg.from_user.id, value=value)
        msg = await msg.answer(text=i18n.text.user.time_stage1())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_video(
        video='https://t.me/sksjkdksnsjdjdndksm/19',
        caption=i18n.text.user.time(),
        reply_markup=get_time_kbd(i18n=i18n)
    )
    await state.set_state(UserMainSG.time)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='enter_time'
    )

@user_router.callback_query(StateFilter(UserMainSG.time))
async def input_time(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    msg = call.message
    if 'back' not in call.data:
        value: str = await rstorage.get(name=call.from_user.id) + f'time:{(call.data)[2:].capitalize()};'
        await rstorage.set(name=call.from_user.id, value=value)
        value: list = [(val.split(':'))[-1] for val in value.split(';')]
        msg = await msg.answer(text=i18n.text.user.standard_check_stage1())
        await asyncio.sleep(2)
    await msg.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/20',
        caption=i18n.text.user.standard_check(
            niche=value[0],
            sources=value[1],
            model=value[2],
            unit_economy=value[3],
            time=value[4]
        ),
        reply_markup=get_send_kbd(i18n=i18n, send_data='send_standard', back_data='back_verif')
    )
    await state.clear()
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='send_standard'
    )

@user_router.callback_query(F.data.startswith('send'))
async def send_data(call: CallbackQuery, i18n: TranslatorRunner, rstorage: Redis, bot: Bot, config: Config, session_maker: async_sessionmaker) -> None:
    first_name: str = call.from_user.first_name
    niche: str = i18n.btn.fastlane() if 'fastlane' in call.data else i18n.btn.standard()
    data = (await rstorage.get(name=call.from_user.id)).split(';')[:-1]
    if call.data == 'send_fastlane':
        meta: str = f'{call.from_user.id}.fastlane.{first_name.replace('.', '')}'
        product = ((data[0]).split(':'))[1]
        await bot.send_video(
            chat_id=config.bot.ADMIN_CHAT,
            video='https://t.me/sksjkdksnsjdjdndksm/4',
            caption=i18n.text.data.fastlane(
                username=f'@{call.from_user.username}',
                product=product
            ),
            reply_markup=get_leadpanel_kbd(i18n=i18n, meta=meta)
        )
    else:
        meta: str = f'{call.from_user.id}.standard.{first_name.replace('.', '')}'
        product: str = ((data[0]).split(':'))[1]
        traffic: str = ((data[1]).split(':'))[1]
        model: str = ((data[2]).split(':'))[1]
        economy: str = ((data[3]).split(':'))[1]
        time: str = ((data[4]).split(':'))[1]
        await bot.send_video(
            chat_id=config.bot.ADMIN_CHAT,
            video='https://t.me/sksjkdksnsjdjdndksm/6',
            caption=i18n.text.data.standard(
                username=f'@{call.from_user.username}',
                niche=product,
                traffic=traffic,
                model=model,
                economy=economy,
                time=time
            ),
            reply_markup=get_leadpanel_kbd(i18n=i18n, meta=meta)
        )
    await call.message.delete()
    msg = await call.message.answer(text=i18n.text.user.compilation1())
    await asyncio.sleep(2)
    await msg.delete()
    msg = await msg.answer(text=i18n.text.user.compilation2())
    await asyncio.sleep(2)
    await msg.delete()
    await msg.answer(
        text=i18n.text.user.data_sent(name=first_name, niche=niche),
        reply_markup=get_success_kbd(i18n=i18n)
    )
    await rstorage.delete(call.from_user.id)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='was sent'
    )

@user_router.callback_query(F.data == 'neurohub')
async def cmd_neurohub(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.user.neurohub(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_start')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='neurohub'
    )

@user_router.callback_query(F.data == 'pro_reactor')
async def cmd_pro_reactor(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.user.pro_reactor(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_start')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pro_reactor'
    )

@user_router.callback_query(F.data == 'traffic')
async def cmd_traffic(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    await call.message.answer(
        text=i18n.text.user.traffic(),
        reply_markup=get_back_kbd(i18n=i18n, callback_data='back_start')
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='traffic'
    )