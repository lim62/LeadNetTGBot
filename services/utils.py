import asyncio

from random import choice
from typing import TYPE_CHECKING
from pyrogram import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram.enums.parse_mode import ParseMode

if (TYPE_CHECKING):
    from app.qt_windows.bot_window import BotWindow

async def account_waiting(self: 'BotWindow', client: Client, wait: int, where: list) -> None:
    await asyncio.sleep(wait)
    where.append(client)

def prepare_text(text: str):
    past_text: str = text
    from_change: list[str] = ['.', '?', ',']
    to_change: list[str] = ['!', '!', ' ']
    if choice([True, False]):
        letter_change: str = choice(from_change)
        to_letter_change = to_change[from_change.index(letter_change)]
        if text:
            text.replace(letter_change, to_letter_change)
    if text:
        if text.strip():
            return text
    else:
        return past_text

async def sending(client: Client, message: any, chat: any, reply_id: int = None) -> int:
    if isinstance(chat, str):
        chat_id = chat
    else:
        chat_id = chat.id
    try:
        if message.media_group_id:
            media: list[InputMediaPhoto | InputMediaVideo] = []
            photos: list[str] = []
            videos: list[str] = []
            captions: list[str] = []
            caption_entities: list = []
            album = await client.get_media_group("me", message_id=message.id)
            for msg in album:
                if msg.photo:
                    photos.append(msg.photo.file_id)
                if msg.video:
                    videos.append(msg.video.file_id)
                if msg.caption:
                    captions.append(prepare_text(msg.caption))
                if msg.caption_entities:
                    caption_entities = msg.caption_entities
            for i, file_id in enumerate(photos):
                if i == 0 and captions:
                    media.append(
                        InputMediaPhoto(
                            file_id,
                            caption=captions[0],
                            caption_entities=caption_entities[0],
                        )
                    )
                else:
                    media.append(InputMediaPhoto(file_id))
            for i, file_id in enumerate(videos):
                if not photos and i == 0 and captions:
                    media.append(
                        InputMediaVideo(
                            file_id,
                            caption=captions[0],
                            caption_entities=caption_entities[0],
                        )
                    )
                else:
                    media.append(InputMediaVideo(file_id))
            msg = await client.send_media_group(
                chat_id=chat_id, media=media, reply_to_message_id=reply_id
            )
        else:
            if message.video:
                msg = await client.send_video(
                    chat_id=chat_id,
                    video=message.video.file_id,
                    caption=prepare_text(message.caption),
                    parse_mode=ParseMode.HTML,
                    caption_entities=message.caption_entities,
                    reply_to_message_id=reply_id,
                )
            elif message.photo:
                msg = await client.send_photo(
                    chat_id=chat_id,
                    photo=message.photo.file_id,
                    caption=prepare_text(message.caption),
                    parse_mode=ParseMode.HTML,
                    caption_entities=message.caption_entities,
                    reply_to_message_id=reply_id,
                )
            else:
                msg = await client.send_message(
                    chat_id=chat_id,
                    text=prepare_text(message.text),
                    parse_mode=ParseMode.HTML,
                    entities=message.entities,
                    reply_to_message_id=reply_id,
                )
        return msg.id
    except Exception:
        await client.send_message(
            chat_id=chat_id,
            text=prepare_text(message.caption),
            parse_mode=ParseMode.HTML,
            reply_to_message_id=reply_id,
        )
        return