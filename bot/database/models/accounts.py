from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, Integer
from bot.database.base import Base

class Account(Base):
    __tablename__ = 'accounts'

    phone: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    api_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    api_hash: Mapped[int] = mapped_column(BigInteger, nullable=False)
    app_version: Mapped[str] = mapped_column(String, nullable=False)
    device_model: Mapped[str] = mapped_column(String, nullable=False)
    system_version: Mapped[str] = mapped_column(String, nullable=False)
    lang_code: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    proxy_scheme: Mapped[str] = mapped_column(String, nullable=False)
    proxy_hostname: Mapped[str] = mapped_column(String, nullable=False)
    proxy_port: Mapped[int] = mapped_column(Integer, nullable=False)
    proxy_username: Mapped[str] = mapped_column(String, nullable=False)
    proxy_password: Mapped[str] = mapped_column(String, nullable=False)