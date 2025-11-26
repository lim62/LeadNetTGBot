from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.dialects.postgresql import insert
from bot.database.models.accounts import Account
from bot.database.models.users import User

async def upsert_user(
    session_maker: async_sessionmaker[AsyncSession],
    telegram_id: int | None = None,
    username: str | None = None,
    status: str | None = None,
    date: str | None = None,
    stage: str | None = None,
    messages: int | None = None,
    have_prepared: bool = None
):
    to_set: dict = {}
    if date is None:
        date = datetime.now().strftime("%H:%M %d.%m.%Y")
    stmt = (
        insert(User)
        .values(
            telegram_id=telegram_id,
            username=username,
            status=status,
            date=date,
            stage=stage,
            messages=messages,
            have_prepared=have_prepared,
        )
    )
    if status and not username:
        to_set['status'] = status
    elif stage and not username:
        to_set['stage'] = stage
    elif messages and not username:
        to_set['messages'] = messages
    elif not username:
        to_set['have_prepared'] = have_prepared
    if to_set:
        stmt = stmt.on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_=to_set
        )
    else:
        stmt = stmt.on_conflict_do_nothing()
    async with session_maker() as session:
        await session.execute(stmt)
        await session.commit()
    
async def get_all_users(session_maker: async_sessionmaker[AsyncSession], telegram_id: int = None) -> list[dict]:
    async with session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id)) if telegram_id else await session.execute(select(User))
        users = result.scalars().all()
        return [
            {
                "telegram_id": u.telegram_id,
                "username": u.username,
                "status": u.status,
                "date": u.date,
                "stage": u.stage,
                "messages": u.messages,
                "have_prepared": u.have_prepared,
            }
            for u in users
        ]

async def upsert_account(
    session_maker: async_sessionmaker[AsyncSession],
    phone: str,
    api_id: int,
    api_hash: str,
    app_version: str,
    device_model: str,
    system_version: str,
    lang_code: str,
    password: str,
    proxy_scheme: str,
    proxy_hostname: str,
    proxy_port: int,
    proxy_username: str,
    proxy_password: str
):
    to_insert = dict(
        phone=phone,
        api_id=api_id,
        api_hash=api_hash,
        app_version=app_version,
        device_model=device_model,
        system_version=system_version,
        lang_code=lang_code,
        password=password,
        proxy_scheme=proxy_scheme,
        proxy_hostname=proxy_hostname,
        proxy_port=proxy_port,
        proxy_username=proxy_username,
        proxy_password=proxy_password
    )
    stmt = (
        insert(Account)
        .values(to_insert)
        .on_conflict_do_update(
            index_elements=[Account.phone],
            set_=to_insert
        )
    )
    async with session_maker() as session:
        await session.execute(stmt)
        await session.commit()

async def delete_account(
    session_maker: async_sessionmaker[AsyncSession],
    phone: str
) -> None:
    stmt = delete(Account).where(Account.phone == phone)
    async with session_maker() as session:
        await session.execute(stmt)
        await session.commit()

async def get_all_accounts(session_maker: async_sessionmaker[AsyncSession]) -> list[dict]:
    async with session_maker() as session:
        result = await session.execute(select(Account))
        accounts = result.scalars().all()
        return [
            {
                "phone": acc.phone,
                "api_id": acc.api_id,
                "api_hash": acc.api_hash,
                "app_version": acc.app_version,
                "device_model": acc.device_model,
                "system_version": acc.system_version,
                "lang_code": acc.lang_code,
                "password": acc.password,
                "proxy_scheme": acc.proxy_scheme,
                "proxy_hostname": acc.proxy_hostname,
                "proxy_port": acc.proxy_port,
                "proxy_username": acc.proxy_username,
                "proxy_password": acc.proxy_password,
            }
            for acc in accounts
        ]

