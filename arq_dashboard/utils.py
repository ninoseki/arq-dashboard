from dataclasses import dataclass
from typing import Set

from arq.constants import default_queue_name
from cache import AsyncTTL

from arq_dashboard.core import settings
from arq_dashboard.queue import Queue


@dataclass
class Metadata:
    functions: Set[str]


@AsyncTTL(time_to_live=settings.CACHE_TTL, maxsize=settings.CACHE_MAX_SIZE)
async def get_metadata(queue_name: str = default_queue_name) -> Metadata:
    queue = Queue.from_name(queue_name)

    jobs = await queue.get_jobs()

    functions: Set[str] = set()

    for job in jobs:
        functions.add(job.function)

    return Metadata(functions=functions)
