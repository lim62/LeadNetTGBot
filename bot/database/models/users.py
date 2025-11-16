from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String
from bot.database.base import Base

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    story: Mapped[str | None] = mapped_column(String, nullable=True)
    design: Mapped[str | None] = mapped_column(String, nullable=True)