from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import Connection, WebSocketManager
from fastapi.websockets import WebSocketDisconnect
from redis.asyncio import Redis

from enums import EventType
from exc import PlayerLeftError
from logger import logger
from schemas import Event

from .handlers import create_handler, execute_action_handler, exit_handler, join_handler


async def websocket_handler(
    connection: Connection, manager: WebSocketManager, redis: Redis, scheduler: AsyncIOScheduler
) -> None:
    while True:
        event = Event.model_validate(await connection.receive_json())

        try:
            await parse_event(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
                scheduler=scheduler,
            )
        except (WebSocketDisconnect, PlayerLeftError):
            logger.debug("Player left")
            return
        except Exception as exc:
            logger.debug(exc)


async def parse_event(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
    scheduler: AsyncIOScheduler,
) -> None:
    match event.type:
        case EventType.CREATE:
            await create_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
                scheduler=scheduler,
            )
        case EventType.EXECUTE_ACTION:
            await execute_action_handler(
                connection=connection, manager=manager, event=event, redis=redis
            )
        case EventType.EXIT:
            await exit_handler(connection=connection, manager=manager, event=event, redis=redis)
        case EventType.JOIN:
            await join_handler(connection=connection, manager=manager, event=event, redis=redis)
