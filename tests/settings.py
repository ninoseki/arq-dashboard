from typing import Optional

from arq.connections import RedisSettings
from starlette.config import Config

config = Config(".env")

REDIS_HOST: str = config("TESTING_REDIS_HOST", cast=str, default="localhost")
REDIS_PORT: int = config("TESTING_REDIS_PORT", cast=int, default=6379)
REDIS_PASSWORD: Optional[str] = config("TESTING_REDIS_PASSWORD", cast=str, default=None)

REDIS_SETTINGS = RedisSettings(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
)
