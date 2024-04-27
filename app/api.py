from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import Connection, WebSocketManager
from fastapi import APIRouter, status
from fastapi.param_functions import Body, Depends, Query
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pokerengine.card import Cards
from pokerengine.evaluation import get_evaluation_result
from redis.asyncio import Redis

from core.depends import get_redis, get_scheduler, get_websocket_manager
from enums import EventType
from exc import PlayerLeftError
from logger import logger
from schemas import ApplicationResponse, Event
from utils.id import generate_id
from ws import handlers

router = APIRouter()


@router.websocket(path="/ws")
async def websocket_handler(
    websocket: WebSocket,
    manager: WebSocketManager = Depends(get_websocket_manager),
    redis: Redis = Depends(get_redis),
    scheduler: AsyncIOScheduler = Depends(get_scheduler),
    id: Optional[str] = Query(None),
) -> None:
    connection = await manager.new_connection(
        websocket=websocket, conn_id=id if id else generate_id()
    )

    try:
        await _websocket_handler(
            connection=connection, manager=manager, redis=redis, scheduler=scheduler
        )
    except Exception:
        manager.remove_connection(connection)


async def _websocket_handler(
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
            await handlers.create_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
                scheduler=scheduler,
            )
        case EventType.EXECUTE_ACTION:
            await handlers.execute_action_handler(
                connection=connection, manager=manager, event=event, redis=redis
            )
        case EventType.EXIT:
            await handlers.exit_handler(
                connection=connection, manager=manager, event=event, redis=redis
            )
        case EventType.JOIN:
            await handlers.join_handler(
                connection=connection, manager=manager, event=event, redis=redis
            )


@router.post(
    path="/getEvaluationResult",
    response_model=ApplicationResponse[List[Tuple[str, int]]],
    status_code=status.HTTP_200_OK,
)
async def get_evaluation_result_handler(
    board: List[str] = Body(...), hands: List[str] = Body(...), players: List[int] = Body(...)
) -> Dict[str, Any]:
    return {
        "ok": True,
        "result": [
            (str(result), index)
            for result, index in get_evaluation_result(
                cards=Cards(board=board, hands=hands), players=players
            )
        ],
    }
