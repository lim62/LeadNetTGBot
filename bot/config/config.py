from pydantic import BaseModel, SecretStr, PostgresDsn
from environs import Env

class BotConfig(BaseModel):
    TOKEN: SecretStr
    ADMINS_IDS: list[int]

class LoggingConfig(BaseModel):
    LEVEL: str
    FORMAT: str

class DatabaseCongig(BaseModel):
    DSN: PostgresDsn

class RedisConfig(BaseModel):
    HOST: str
    PORT: int

class Config(BaseModel):
    bot: BotConfig
    log: LoggingConfig
    database: DatabaseCongig
    redis: RedisConfig

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(override=True)
    return Config(
        bot=BotConfig(
            TOKEN=env('TOKEN'),
            ADMINS_IDS=env.list('ADMINS_IDS')
        ),
        log=LoggingConfig(
            LEVEL=env('LOGGING_LEVEL'),
            FORMAT=env('LOGGING_FORMAT')
        ),
        database=DatabaseCongig(
            DSN=env('POSTGRES_DSN')
        ),
        redis=RedisConfig(
            HOST=env('REDIS_HOST'),
            PORT=env.int('REDIS_PORT')
        )
    )