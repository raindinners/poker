from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import WebSocketManager
from fastapi.websockets import WebSocket
from redis.asyncio import Redis


def get_redis(websocket: WebSocket) -> Redis:
    return websocket.app.state.redis


def get_websocket_manager(websocket: WebSocket) -> WebSocketManager:
    return websocket.app.state.manager


def get_scheduler(websocket: WebSocket) -> AsyncIOScheduler:
    return websocket.app.state.scheduler
