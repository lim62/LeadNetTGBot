from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String
from bot.database.base import Base

class Admin(Base):
    __tablename__ = 'admins'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    mailing_text: Mapped[str] = mapped_column(String, nullable=True)
    photo: Mapped[str] = mapped_column(String, nullable=True)