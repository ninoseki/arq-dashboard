from .api_model import APIModel
from .mixins import CachedAtMixin


class Queue(APIModel):
    name: str


class QueueStats(CachedAtMixin, APIModel):
    name: str
    host: str
    port: int
    database: int

    queued_jobs: int
    in_progress_jobs: int
    deferred_jobs: int
    complete_jobs: int
    not_found_jobs: int
