import asyncio
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Callable, List, Optional, Sequence, Union
from unittest.mock import AsyncMock

import pytest
from arq import ArqRedis, Worker
from arq.constants import job_key_prefix
from arq.jobs import Job
from arq.typing import WorkerCoroutine
from arq.worker import Function
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from arq_dashboard import create_app
from arq_dashboard.dependencies import get_redis

from .settings import REDIS_SETTINGS


@pytest.fixture
async def redis() -> AsyncGenerator[ArqRedis, None]:
    async with get_redis(REDIS_SETTINGS) as redis:
        await redis.flushall()
        yield redis


@pytest.fixture
async def create_worker(
    redis: ArqRedis,
) -> AsyncGenerator[Callable[[Any], Worker], None]:
    worker: Optional[Worker] = None

    def create(
        functions: Sequence[Union[Function, WorkerCoroutine]], **kwargs: Any
    ) -> Worker:
        nonlocal worker
        worker = Worker(
            functions=functions,
            redis_pool=redis,
            burst=True,
            max_burst_jobs=100,
            poll_delay=0,
            **kwargs,
        )
        return worker

    yield create

    if worker:
        await worker.close()


async def deferred_task(_ctx: Any) -> None:
    pass


async def running_task(_ctx: Any) -> None:
    await asyncio.sleep(0.2)


async def successful_task(_ctx: Any) -> None:
    pass


async def failed_task(_ctx: Any) -> None:
    raise Exception


@dataclass
class JobsCreator:
    worker: Worker
    redis: ArqRedis

    async def create_queued(self) -> Job:
        job = await self.redis.enqueue_job("successful_task")
        assert job
        return job

    async def create_running(self) -> Job:
        job = await self.redis.enqueue_job("running_task")
        assert job
        with suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self.worker.main(), 0.1)
        return job

    async def create_deferred(self) -> Job:
        job = await self.redis.enqueue_job("deferred_task", _defer_by=9000)
        assert job
        return job

    async def create_unserializable(self) -> Job:
        job = await self.redis.enqueue_job("successful_task")
        assert job
        await self.redis.set(job_key_prefix + job.job_id, "RANDOM TEXT")
        return job


@pytest.fixture
async def jobs_creator(redis: ArqRedis, create_worker: Any) -> JobsCreator:
    worker = create_worker(
        functions=[deferred_task, running_task, successful_task, failed_task]
    )
    return JobsCreator(worker=worker, redis=redis)


@pytest.fixture
async def all_jobs(jobs_creator: JobsCreator) -> List[Job]:
    # the order matters
    return [
        await jobs_creator.create_running(),
        await jobs_creator.create_deferred(),
        await jobs_creator.create_queued(),
    ]


@pytest.fixture
async def unserializable_job(jobs_creator: JobsCreator) -> Job:
    return await jobs_creator.create_unserializable()


@pytest.fixture
async def client(mocker: MockerFixture, redis: ArqRedis):
    async def override_get_redis(_setting):
        yield redis

    mocked = mocker.patch("arq_dashboard.queue.get_redis")
    mocked.return_value.__aenter__.return_value = AsyncMock(
        side_effect=override_get_redis
    )

    app = create_app()
    return TestClient(app)
