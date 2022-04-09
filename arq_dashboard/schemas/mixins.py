from datetime import datetime

import arrow
from pydantic import BaseModel, Field


def get_cached_at():
    return arrow.utcnow().datetime


class CachedAtMixin(BaseModel):
    cached_at: datetime = Field(default_factory=get_cached_at)


class PaginationMixin(BaseModel):
    total: int
    page_size: int
    current_page: int
