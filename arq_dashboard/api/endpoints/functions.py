from typing import List, cast

from fastapi import APIRouter, Depends

from arq_dashboard import schemas
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.utils import Metadata, get_metadata

router = APIRouter()


@router.get("/", response_model=List[schemas.Function])
async def get_functions(
    queue_name: str = Depends(get_queue_name),
) -> List[schemas.Function]:
    metadata = cast(Metadata, await get_metadata(queue_name))
    return [schemas.Function(name=name) for name in metadata.functions]
