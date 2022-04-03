from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .api.api import api_router
from .core import settings
from .errors import ArqDashboardError, InvalidQueueNameError


def handle_arq_dashboard_error(_request: Request, error: ArqDashboardError):
    if isinstance(error, InvalidQueueNameError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(error)},
        )

    return JSONResponse(
        status_code=500,
        content={"detail": str(error)},
    )


def create_app() -> FastAPI:
    logger.add(
        settings.LOG_FILE, level=settings.LOG_LEVEL, backtrace=settings.LOG_BACKTRACE
    )

    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
    )

    # add middle wares
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # add routers
    app.include_router(api_router, prefix="/api")

    app.add_exception_handler(ArqDashboardError, handle_arq_dashboard_error)

    app.mount(
        "/",
        StaticFiles(
            html=True,
            directory=Path(
                __file__,
            ).parent
            / "./frontend/",
        ),
        name="static",
    )

    return app
