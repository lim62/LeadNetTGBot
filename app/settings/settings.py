import random
import asyncio

from redis import Redis
from pyrogram import Client
from pyrogram.enums import ParseMode
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.database.requests import get_all_accounts, upsert_account

async def start_clients(session_maker: async_sessionmaker, rstorage: Redis) -> None:
    clients: list[Client] = [
        Client(
            name=account['phone'][1:],
            api_id=account['api_id'],
            api_hash=account['api_hash'],
            app_version=account['app_version'],
            device_model=account['device_model'],
            system_version=account['system_version'],
            lang_code=account['lang_code'],
            phone_number=account['phone'],
            password=account['password'],
            parse_mode=ParseMode.HTML,
            workdir='sessions',
            proxy=dict(
                scheme=account['proxy_scheme'],
                hostname=account['proxy_hostname'],
                port=int(account['proxy_port']),
                username=account['proxy_username'],
                password=account['proxy_password']
            )
        )
        for account in await get_all_accounts(session_maker=session_maker)
    ]
    for client in clients:
        asyncio.gather(schedule_starting(client=client, rstorage=rstorage))
    return clients
    
async def schedule_starting(client: Client, rstorage: Redis) -> None:
    await asyncio.sleep(random.uniform(1, 10))
    await client.start(rstorage=rstorage)

async def add_client(data: str, rstorage: Redis, session_maker: async_sessionmaker, clients: list[Client]) -> None:
    client: Client = Client(
        name=data['phone'][1:],
        api_id=data['api_id'],
        api_hash=data['api_hash'],
        app_version=data['app_version'],
        device_model=data['device_model'],
        system_version=data['system_version'],
        lang_code=data['lang_code'],
        phone_number=data['phone'],
        password=data['password'],
        parse_mode=ParseMode.HTML,
        workdir='sessions',
        proxy=dict(
            scheme=data['proxy_scheme'],
            hostname=data['proxy_hostname'],
            port=int(data['proxy_port']),
            username=data['proxy_username'],
            password=data['proxy_password']
        )
    )
    try:
        await client.start(rstorage=rstorage)
        await upsert_account(
            session_maker=session_maker,
            phone=data['phone'],
            api_id=data['api_id'],
            api_hash=data['api_hash'],
            app_version=data['app_version'],
            device_model=data['device_model'],
            system_version=data['system_version'],
            lang_code=data['lang_code'],
            password=data['password'],
            proxy_scheme=data['proxy_scheme'],
            proxy_hostname=data['proxy_hostname'],
            proxy_port=int(data['proxy_port']),
            proxy_username=data['proxy_username'],
            proxy_password=data['proxy_password']
        )
        clients.append(client)
    except Exception as e:
        print(e)
        raise e()