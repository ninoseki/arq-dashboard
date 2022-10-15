import sys
from typing import Optional, TextIO

from arq.connections import RedisSettings
from arq.constants import default_queue_name
from arq.jobs import Deserializer
from starlette.config import Config

from .datastructures import DatabaseURL

config = Config(".env")

# general settings
PROJECT_NAME: str = config("ARQ_DASHBOARD_PROJECT_NAME", default="arq-dashboard")

DEBUG: bool = config("ARQ_DASHBOARD_DEBUG", cast=bool, default=False)
TESTING: bool = config("ARQ_DASHBOARD_TESTING", cast=bool, default=False)

# log settings
LOG_FILE: TextIO = config("ARQ_DASHBOARD_LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("ARQ_DASHBOARD_LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("ARQ_DASHBOARD_LOG_BACKTRACE", cast=bool, default=True)

# Redis & ARQ settings
REDIS_URL: DatabaseURL = config(
    "ARQ_DASHBOARD_REDIS_URL", cast=DatabaseURL, default="redis://localhost:6379"
)
ARQ_DESERIALIZER: Optional[Deserializer] = None

ARQ_QUEUES = {
    default_queue_name: RedisSettings(
        host=str(REDIS_URL.hostname),
        port=REDIS_URL.port or 6379,
        password=REDIS_URL.password,
    )
}

MAX_AT_ONCE: Optional[int] = config("ARQ_DASHBOARD_MAX_AT_ONCE", cast=int, default=10)
MAX_PER_SECONDS: Optional[int] = config(
    "ARQ_DASHBOARD_MAX_PER_SECONDS", cast=int, default=None
)

CACHE_TTL: int = config("ARQ_DASHBOARD_CACHE_TTL", cast=int, default=60)
CACHE_MAX_SIZE: int = config("ARQ_DASHBOARD_CACHE_MAX_SIZE", cast=int, default=32)
