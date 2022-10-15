from datetime import datetime

import arrow
from pydantic import Field

from .api_model import APIModel


def get_cached_at():
    return arrow.utcnow().datetime


class CachedAtMixin(APIModel):
    cached_at: datetime = Field(default_factory=get_cached_at)


class PaginationMixin(APIModel):
    total: int
    page_size: int
    current_page: int
