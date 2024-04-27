from __future__ import annotations

from typing import Any, Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import WebSocketManager
from fastapi import FastAPI, status
from redis.asyncio import Redis

from api import router as api_router
from core.exc import create_exception_handlers
from core.middleware import create_middleware
from core.settings import redis_settings, server_settings
from logger import logger
from schemas import ApplicationResponse


def create_application() -> FastAPI:
    """
    Setup FastAPI application: middleware, exception handlers, jwt, logger.
    """

    docs_url, redoc_url, openapi_url = "/poker/docs", "/poker/redoc", "/poker/openapi.json"
    if not server_settings.DEBUG:
        docs_url, redoc_url, openapi_url = None, None, None

    application = FastAPI(
        title="raindinners.poker",
        description="Backend for playing poker via websockets.",
        version="1.0a",
        debug=server_settings.DEBUG,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )
    application.include_router(api_router, tags=["poker"], prefix="/poker")

    redis = Redis(host=redis_settings.REDIS_HOSTNAME, port=redis_settings.REDIS_PORT)
    manager = WebSocketManager(redis_settings.REDIS_CHANNEL, redis_settings.url)
    scheduler = AsyncIOScheduler()

    application.state.redis = redis
    application.state.manager = manager
    application.state.scheduler = scheduler

    def create_on_event() -> None:
        @application.on_event("startup")
        async def startup() -> None:
            logger.info("Application startup")

        @application.on_event("shutdown")
        async def shutdown() -> None:
            logger.warning("Application shutdown")

        @application.on_event("startup")
        async def manager_startup() -> None:
            await manager.startup()

        @application.on_event("shutdown")
        async def manager_shutdown() -> None:
            await manager.shutdown()

        @application.on_event("startup")
        async def scheduler_startup() -> None:
            scheduler.start()

    def create_routes() -> None:
        @application.post(
            path="/poker",
            response_model=ApplicationResponse[bool],
            status_code=status.HTTP_200_OK,
        )
        async def healthcheck() -> Dict[str, Any]:
            return {
                "ok": True,
                "result": True,
            }

    create_exception_handlers(application=application)
    create_middleware(application=application)
    create_on_event()
    create_routes()

    return application


app = create_application()
