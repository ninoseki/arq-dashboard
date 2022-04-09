from datetime import datetime

from pydantic import BaseModel, Field


class CachedAtMixin(BaseModel):
    cached_at: datetime = Field(default=datetime.utcnow())
