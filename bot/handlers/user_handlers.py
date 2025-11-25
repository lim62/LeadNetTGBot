import asyncio

from redis import Redis
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaVideo, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.config import Config
from bot.states import UserMainSG
from bot.database.requests import upsert_user
from bot.keyboards import (
    get_start_kbd, get_back_kbd, get_verif_kbd, 
    get_fastlane_kbd, get_delta_kbd, get_send_kbd,
    get_success_kbd, get_standard_kbd, get_time_kbd,
    get_leadpanel_kbd, get_pulse_kbd, get_tarif_kbd,
    get_workpulse_kbd, get_offer_kdb, get_zalp_kbd,
    get_afterzalp_kbd
)

user_router = Router()

@user_router.message(CommandStart())
@user_router.callback_query(F.data == 'back_start')
async def cmd_start(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    first_name: str = msg.from_user.first_name
    if isinstance(obj, Message):
        msg = await msg.answer(text=i18n.text.user.start_stage1())
        await asyncio.sleep(2)
        msg = await msg.edit_text(text=i18n.text.user.start_stage2())
        await asyncio.sleep(2)
        msg = await msg.edit_text(text=i18n.text.user.start_stage3())
        await asyncio.sleep(2)
    await msg.edit_media(media=InputMediaVideo(media='https://t.me/sksjkdksnsjdjdndksm/10'))
    await msg.edit_caption(caption=i18n.text.user.menu(name=first_name))
    await msg.edit_reply_markup(reply_markup=get_start_kbd(i18n=i18n))
    await state.clear()
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        username=f'@{obj.from_user.username}',
        stage='menu',
        messages=200,
        offer='Something',
        stories='Som',
        from_ref=False
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

@user_router.callback_query(F.data == 'pusk_prepare')
async def cmd_pusk_prepare(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    msg = await call.message.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/27',
        caption=i18n.text.user.pusk_prepare()
    )
    await msg.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, down='how_works_pulse', have_up=False))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pusk_prepare'
    )

@user_router.callback_query(F.data == 'how_works_pulse')
async def cmd_what_stage11(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.how_works_pulse()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='pusk_prepare', down='tg_chats'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'tg_chats')
async def cmd_what_stage12(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/24',
            caption=i18n.text.user.tg_chats()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='how_works_pulse', down='offer_pulse'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'offer_pulse')
async def cmd_what_stage22(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/23',
            caption=i18n.text.user.offer_pulse()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_offer_kdb(i18n=i18n))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'test_zalp')
async def cmd_what_stage33(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.test_zalp()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='offer_pulse', down='give_chats', down_text=i18n.btn.zalp()))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'give_chats')
async def cmd_what_stage44(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.give_chats()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='test_zalp', down='upload_chats', down_text=i18n.btn.upload()))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'upload_chats')
async def cmd_what_stage55(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.upload_chats()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='give_chats', have_down=False))
    await state.set_state(UserMainSG.load_chats)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.message(StateFilter(UserMainSG.load_chats))
@user_router.callback_query(F.data == 'msg_zalp')
async def cmd_load_chats(obj: Message | CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    ide = obj.from_user.id
    links = [link.strip() for link in msg.text.split('\n') if link.startswith('http')] + [f'https://{link.strip()}' for link in msg.text.split('\n') if link.startswith('t.me')]
    if isinstance(obj, CallbackQuery):
        await obj.message.delete()
    if len(links) == 0:
        await msg.answer(
            text=i18n.text.user.no_links(),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse1')
        )
    elif len(links) > 100:
        await msg.answer(
            text=i18n.text.user.much_links(),
            reply_markup=get_back_kbd(i18n=i18n, callback_data='back_pulse1')
        )
    else:
        await msg.answer_photo(
            photo='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.msg_zalp(),
            reply_markup=get_workpulse_kbd(i18n=i18n, up='use_own', down='start_zalp', down_text=i18n.btn.use_standard(), up_text=i18n.btn.use_own())
        )
        await state.clear()
    await upsert_user(
        session_maker=session_maker,
        telegram_id=ide,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'use_own')
async def cmd_use_own(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.use_own(),
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='msg_zalp', have_down=False))
    await state.set_state(UserMainSG.load_offer)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.message(StateFilter(UserMainSG.load_offer))
@user_router.callback_query(F.data == 'start_zalp')
async def cmd_start_zalp(obj: Message | CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    msg = obj if isinstance(obj, Message) else obj.message
    if not isinstance(obj, Message):
        await obj.message.delete()
    await msg.answer_photo(
        photo='https://t.me/sksjkdksnsjdjdndksm/28',
        caption=i18n.text.user.start_zalp(),
        reply_markup=get_zalp_kbd(i18n=i18n)
    )
    await upsert_user(
        session_maker=session_maker,
        telegram_id=obj.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'zalp_done')
async def cmd_zalp_done(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.delete()
    msg = await call.message.answer(text=i18n.text.user.flow())
    await asyncio.sleep(2)
    await msg.edit_text(text=i18n.text.user.pulse_going())
    await asyncio.sleep(2)
    await msg.edit_text(text=i18n.text.user.pulse_live())
    await asyncio.sleep(2)
    msg = await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.zalp_done()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_afterzalp_kbd(i18n=i18n))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'continue_prepare')
async def cmd_continue_prepare(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.how_works_continue()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, down='accs_prepare', have_up=False))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'accs_prepare')
async def cmd_accs_prepare(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.accs_prepare()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='how_works_continue', down='antispam'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'antispam')
async def cmd_antispam(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.antispam()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='accs_prepare', down='base_pulse'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'base_pulse')
async def cmd_base_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.base_pulse()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='antispam', down='benifits_pulse'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'benifits_pulse')
async def cmd_benifits_pulse(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/28',
            caption=i18n.text.user.benifits_pulse()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_workpulse_kbd(i18n=i18n, up='base_pulse', down='what66'))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse'
    )

@user_router.callback_query(F.data == 'tarifs')
@user_router.callback_query(F.data == 'back_tarifs')
async def cmd_tarifs(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/24',
            caption=i18n.text.user.tarifs()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_tarif_kbd(i18n=i18n))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='pulse_tarifs'
    )

@user_router.callback_query(F.data == 'pulse_threedays')
async def cmd_threedays(call: CallbackQuery, i18n: TranslatorRunner) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/24',
            caption=i18n.text.user.pulse_threedays()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs'))

@user_router.callback_query(F.data == 'pulse_tendays')
async def cmd_tendays(call: CallbackQuery, i18n: TranslatorRunner) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/24',
            caption=i18n.text.user.pulse_tendays()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs'))

@user_router.callback_query(F.data == 'pulse_month')
async def cmd_monthdays(call: CallbackQuery, i18n: TranslatorRunner) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/24',
            caption=i18n.text.user.pulse_month()
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_tarifs'))

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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/11',
            caption=i18n.text.user.verification(name=call.from_user.first_name)
        )
    )
    await msg.edit_reply_markup(reply_markup=get_verif_kbd(i18n=i18n))
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='verification'
    )

@user_router.callback_query(F.data == 'fastlane')
@user_router.callback_query(F.data == 'back_fastlane')
async def cmd_fastlane(call: CallbackQuery, i18n: TranslatorRunner, state: FSMContext, rstorage: Redis, session_maker: async_sessionmaker) -> None:
    try:
        await rstorage.delete(call.from_user.id)
    except Exception:
        pass
    if call.data == 'fastlane':
        await call.message.delete()
        msg = await call.message.answer(text=i18n.text.user.fastlane_stage1())
        await asyncio.sleep(2)
        msg = await msg.edit_text(text=i18n.text.user.fastlane_stage2())
        await asyncio.sleep(2)
    else:
        msg = call.message
    await msg.edit_media(
        media=InputMediaVideo(
            media='https://t.me/sksjkdksnsjdjdndksm/12',
            caption=i18n.text.user.fastlane(name=call.from_user.first_name)
        )
    )
    await msg.edit_reply_markup(reply_markup=get_fastlane_kbd(i18n=i18n))
    await state.set_state(UserMainSG.fastlane)
    await upsert_user(
        session_maker=session_maker,
        telegram_id=call.from_user.id,
        stage='fastlane'
    )

@user_router.callback_query(F.data == 'delta')
async def cmd_delta(call: CallbackQuery, i18n: TranslatorRunner, session_maker: async_sessionmaker) -> None:
    await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/13',
            caption=i18n.text.user.delta(name=call.from_user.first_name)
        )
    )
    await call.message.edit_reply_markup(reply_markup=get_delta_kbd(i18n=i18n))
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
    msg = await msg.edit_text(text=i18n.text.user.fastlane_send2())
    await asyncio.sleep(2)
    await msg.edit_text(
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
    msg = await call.message.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/14',
            caption=i18n.text.user.standard(name=call.from_user.first_name)
        )
    )
    await msg.edit_reply_markup(reply_markup=get_standard_kbd(i18n=i18n))
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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/15',
            caption=i18n.text.user.product()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_verif'))
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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/16',
            caption=i18n.text.user.sources_traffic()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_product'))
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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/17',
            caption=i18n.text.user.model()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_traffic'))
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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/18',
            caption=i18n.text.user.economics()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_back_kbd(i18n=i18n, callback_data='back_model'))
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
    await msg.edit_media(
        media=InputMediaVideo(
            media='https://t.me/sksjkdksnsjdjdndksm/19',
            caption=i18n.text.user.time()
        )
    )
    await msg.edit_reply_markup(reply_markup=get_time_kbd(i18n=i18n))
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
    await msg.edit_media(
        media=InputMediaPhoto(
            media='https://t.me/sksjkdksnsjdjdndksm/20',
            caption=i18n.text.user.standard_check(
                niche=value[0],
                sources=value[1],
                model=value[2],
                unit_economy=value[3],
                time=value[4]
            )
        )
    )
    await msg.edit_reply_markup(reply_markup=get_send_kbd(i18n=i18n, send_data='send_standard', back_data='back_verif'))
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
    msg = await msg.edit_text(text=i18n.text.user.compilation2())
    await asyncio.sleep(2)
    await msg.edit_text(
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