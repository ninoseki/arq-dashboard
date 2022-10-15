from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from arq import ArqRedis, create_pool
from arq.connections import RedisSettings
from arq.constants import default_queue_name
from fastapi import Header


@asynccontextmanager
async def get_redis(settings: RedisSettings) -> AsyncGenerator[ArqRedis, None]:
    redis: Optional[ArqRedis] = None

    try:
        redis = await create_pool(settings_=settings)
        yield redis
    finally:
        if redis is None:
            return

        await redis.close()


def get_queue_name(
    arq_queue_name: Optional[str] = Header(default=None, description="ARQ queue name"),
) -> str:
    return arq_queue_name or default_queue_name
