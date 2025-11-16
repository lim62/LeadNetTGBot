from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from bot.database.models.admins import Admin
from bot.database.models.users import User

async def insert_admin(
    session: AsyncSession,
    telegram_id: int,
    mailing_text: str,
    photo: str
) -> None:
    stmt = insert(Admin).values(
        dict(
            telegram_id=telegram_id,
            mailing_text=mailing_text,
            photo=photo
        )
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            mailing_text=mailing_text,
            photo=photo
        )
    )
    await session.execute(stmt)
    await session.commit()

async def insert_text(
    session: AsyncSession,
    telegram_id: int,
    mailing_text: str
) -> None:
    stmt = update(Admin).where(Admin.telegram_id == telegram_id).values(dict(mailing_text=mailing_text))
    await session.execute(stmt)
    await session.commit()

async def insert_photo(
    session: AsyncSession,
    telegram_id: int,
    photo: str
) -> None:
    stmt = update(Admin).where(Admin.telegram_id == telegram_id).values(dict(photo=photo))
    await session.execute(stmt)
    await session.commit()

async def select_admin(
    session: AsyncSession
) -> dict:
    stmt = select(Admin)
    result = await session.execute(stmt)
    return result.scalars().all()

async def insert_user(
    session: AsyncSession,
    telegram_id: int,
    username: str,
    name: str,
    age: str,
    story: str,
    design: str
) -> None:
    stmt = insert(User).values(
        {
            'telegram_id': telegram_id,
            'username': username,
            'name': name,
            'age': age,
            'story': story,
            'design': design
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            username=username,
            name=name,
            age=age,
            story=story,
            design=design
        )
    )
    await session.execute(stmt)
    await session.commit()

async def insert_name(
    session: AsyncSession,
    telegram_id: int,
    name: str
) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values({'name': name})
    await session.execute(stmt)
    await session.commit()

async def insert_age(
    session: AsyncSession,
    telegram_id: int,
    age: str
) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values({'age': age})
    await session.execute(stmt)
    await session.commit()

async def insert_story(
    session: AsyncSession,
    telegram_id: int,
    story: str
) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values({'story': story})
    await session.execute(stmt)
    await session.commit()

async def insert_design(
    session: AsyncSession,
    telegram_id: int,
    design: str
) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values({'design': design})
    await session.execute(stmt)
    await session.commit()

async def update_user(
    session: AsyncSession,
    telegram_id: int,
    name: str = None,
    age: str = None,
    story: str = None,
    design: str = None
) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values(
                                                                        {
                                                                            'name': name,
                                                                            'age': age,
                                                                            'story': story,
                                                                            'design': design
                                                                        }
                                                                      )
    await session.execute(stmt)
    await session.commit()

async def select_user(
    session: AsyncSession
) -> dict:
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()