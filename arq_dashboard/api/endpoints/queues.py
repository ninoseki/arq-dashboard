from typing import List

from fastapi import APIRouter

from arq_dashboard import schemas
from arq_dashboard.core import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Queue])
async def get_queues() -> List[schemas.Queue]:
    keys = settings.ARQ_QUEUES.keys()
    return [schemas.Queue(name=name) for name in keys]
