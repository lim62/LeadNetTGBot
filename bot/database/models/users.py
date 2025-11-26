from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, Boolean
from bot.database.base import Base

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[str | None] = mapped_column(String, nullable=True)
    stage: Mapped[str | None] = mapped_column(String, nullable=True)
    messages: Mapped[int | None] = mapped_column(String, nullable=True)
    have_prepared: Mapped[bool | None] = mapped_column(Boolean, nullable=True)