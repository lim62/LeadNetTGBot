from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, Boolean
from bot.database.base import Base

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    stage: Mapped[str] = mapped_column(String, nullable=False)
    messages: Mapped[int] = mapped_column(String, nullable=False)
    offer: Mapped[str | None] = mapped_column(String, nullable=True)
    stories: Mapped[str | None] = mapped_column(String, nullable=True)
    from_ref: Mapped[bool] = mapped_column(Boolean, nullable=False)