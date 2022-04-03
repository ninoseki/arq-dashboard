from fastapi import APIRouter, Depends

from arq_dashboard import schemas
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.queue import Queue

router = APIRouter()


@router.get(
    "/",
    response_model=schemas.QueueStats,
)
async def get_stats(
    queue_name: str = Depends(get_queue_name),
) -> schemas.QueueStats:
    queue = Queue.from_name(queue_name)
    return await queue.get_stats()
