from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from arq.jobs import JobDef as ArqJobDef
from arq.jobs import JobResult, JobStatus

from .api_model import APIModel
from .mixins import CachedAtMixin, PaginationMixin


class JobDef(APIModel):
    function: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    job_try: Optional[int]
    enqueue_time: Optional[datetime]
    score: Optional[int]


class JobInfo(JobDef):
    job_id: str
    success: bool = False

    queue_name: Optional[str] = None
    result: Optional[Any] = None
    start_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None

    status: JobStatus = JobStatus.queued

    @classmethod
    def from_base(
        cls, base_info: Union[ArqJobDef, JobDef, JobResult], job_id: str
    ) -> "JobInfo":
        obj = cls(
            job_id=job_id,
            function=base_info.function,
            args=base_info.args,
            kwargs=base_info.kwargs,
            job_try=base_info.job_try,
            enqueue_time=base_info.enqueue_time,
            score=base_info.score,
        )

        if isinstance(base_info, JobResult):
            obj.success = base_info.success
            obj.result = base_info.result
            obj.start_time = base_info.start_time
            obj.finish_time = base_info.finish_time
            obj.queue_name = base_info.queue_name

        return obj


class CachedJobInfo(CachedAtMixin, JobInfo, APIModel):
    pass


class JobsWithPagination(CachedAtMixin, PaginationMixin, APIModel):
    jobs: List[JobInfo]
