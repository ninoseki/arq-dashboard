from datetime import datetime
from typing import List, Optional

from arq.jobs import JobStatus
from fastapi import APIRouter, Depends, HTTPException, Query

from arq_dashboard import schemas
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.queue import Queue

router = APIRouter()


def filter_by_start_time(job: schemas.JobInfo, start_time: Optional[datetime]):
    if start_time is None:
        return True

    if job.start_time is None:
        return True

    return job.start_time >= start_time


def filter_by_finish_time(job: schemas.JobInfo, finish_time: Optional[datetime]):
    if finish_time is None:
        return True

    if job.finish_time is None:
        return True

    return job.finish_time <= finish_time


def filter_by_function(job: schemas.JobInfo, func: Optional[str]):
    if func is None:
        return True

    return job.function == func


def filter_by_queue_name(
    job: schemas.JobInfo, queue_name: str, *, allow_none_queue_name=True
):
    if job.queue_name is None and allow_none_queue_name is True:
        return True

    return job.queue_name == queue_name


def filter_by_success(job: schemas.JobInfo, success: Optional[bool]):
    if success is None:
        return True

    return job.success is success


def filter_by_limit_and_offset(jobs: List[schemas.JobInfo], limit: int, offset: int):
    return jobs[offset : offset + limit]


def apply_filters(
    jobs: List[schemas.JobInfo],
    *,
    queue_name: str,
    allow_none_queue_name: bool = True,
    success: Optional[bool] = None,
    start_time: Optional[datetime] = None,
    finish_time: Optional[datetime] = None,
    function_name: Optional[str] = None,
) -> List[schemas.JobInfo]:
    filtered_jobs: List[schemas.JobInfo] = []

    for job in jobs:
        if not filter_by_queue_name(
            job, queue_name, allow_none_queue_name=allow_none_queue_name
        ):
            continue

        if not filter_by_success(job, success):
            continue

        if not filter_by_function(job, function_name):
            continue

        if not filter_by_start_time(job, start_time):
            continue

        if not filter_by_finish_time(job, finish_time):
            continue

        filtered_jobs.append(job)

    return filtered_jobs


@router.get("/", response_model=schemas.JobsWithPagination)
async def get_jobs(
    page: int = 1,
    success: Optional[bool] = None,
    status: Optional[JobStatus] = None,
    start_time: Optional[datetime] = Query(None, alias="startTime"),
    finish_time: Optional[datetime] = Query(None, alias="finishTime"),
    function_name: Optional[str] = Query(None, alias="functionName"),
    *,
    queue_name: str = Depends(get_queue_name),
) -> schemas.JobsWithPagination:
    queue = Queue.from_name(queue_name)
    jobs = await queue.get_jobs(status=status)

    # filter jobs by conditions
    filtered_jobs = apply_filters(
        jobs,
        queue_name=queue_name,
        success=success,
        start_time=start_time,
        finish_time=finish_time,
        function_name=function_name,
    )

    # set pagination params
    limit = 100
    offset = (page - 1) * limit
    total = len(jobs)
    filtered_and_paginated_jobs = filter_by_limit_and_offset(
        filtered_jobs, limit, offset
    )

    return schemas.JobsWithPagination(
        jobs=filtered_and_paginated_jobs, total=total, currentPage=page, page_size=limit
    )


@router.get(
    "/{id}",
    response_model=schemas.JobInfo,
)
async def get_job_by_id(
    id: str, *, queue_name: str = Depends(get_queue_name)
) -> schemas.JobInfo:
    queue = Queue.from_name(queue_name)
    job = await queue.get_job_by_id(id)

    if job.status == "not_found":
        raise HTTPException(status_code=404, detail=f"Job:{id} not found")

    return job
