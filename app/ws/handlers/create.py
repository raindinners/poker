from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import Connection, Message, WebSocketManager
from pokerengine.engine import EngineTraits
from redis.asyncio import Redis

from _redis import save
from core.poker import game
from poker import Poker
from schemas import ApplicationResponse, Event
from utils.id import generate_id
from ws.requests import CreateRequest

from ._parser import update_event


def send_game_created(
    connection: Connection, manager: WebSocketManager, poker: str, event: Event
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[str](
                ok=True, result=poker, event_type=event.type
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        ),
    )


async def create_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
    scheduler: AsyncIOScheduler,
) -> None:
    event = update_event(event=event, class_type=CreateRequest)

    poker = generate_id()
    await save(
        redis=redis,
        key=poker,
        value=Poker(
            traits=EngineTraits(
                sb_bet=event.request.sb_bet,
                bb_bet=event.request.bb_bet,
                bb_mult=event.request.bb_mult,
                min_raise=event.request.min_raise,
            )
        ),
    )

    send_game_created(connection=connection, manager=manager, poker=poker, event=event)
    scheduler.add_job(
        game,
        kwargs={
            "manager": manager,
            "redis": redis,
            "poker": poker,
        },
        trigger="interval",
        id=poker,
        max_instances=1,
        seconds=1,
    )
