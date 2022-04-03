from typing import List
from unittest.mock import MagicMock, patch

import pytest
from arq.constants import default_queue_name
from arq.jobs import DeserializationError, Job, JobStatus

from arq_dashboard.queue import Queue

from .conftest import JobsCreator
from .settings import REDIS_SETTINGS


@pytest.mark.asyncio
async def test_all_get_jobs(all_jobs: List[Job]) -> None:
    queue = Queue(default_queue_name, REDIS_SETTINGS)
    assert len(await queue.get_jobs()) == 3


@pytest.mark.asyncio
async def test_status_filter(all_jobs: List[Job]) -> None:
    queue = Queue(default_queue_name, REDIS_SETTINGS)
    assert len(await queue.get_jobs(JobStatus.deferred)) == 1
    assert len(await queue.get_jobs(JobStatus.in_progress)) == 1
    assert len(await queue.get_jobs(JobStatus.queued)) == 1


@pytest.mark.asyncio
async def test_stats(all_jobs: List[Job]) -> None:
    queue = Queue(default_queue_name, REDIS_SETTINGS)
    stats = await queue.get_stats()

    assert stats.name == default_queue_name
    assert stats.queued_jobs == 1
    assert stats.in_progress_jobs == 1
    assert stats.deferred_jobs == 1


@pytest.mark.asyncio
@patch.object(Job, "info")
async def test_deserialize_error(
    mocked_job_info: MagicMock, jobs_creator: JobsCreator
) -> None:
    job = await jobs_creator.create_queued()
    mocked_job_info.side_effect = DeserializationError()

    queue = Queue(default_queue_name, REDIS_SETTINGS)
    job_info = await queue.get_job_by_id(job.job_id)
    assert job_info.function == "unknown (unable to deserialize job)"
