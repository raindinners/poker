from __future__ import annotations

from distributed_websocket import Connection, Message, WebSocketManager
from pokerengine.engine import PlayerAction
from pokerengine.enums import ActionE, PositionE
from redis.asyncio import Redis

from _redis import save
from schemas import ApplicationResponse, Event
from utils.poker import get_poker
from ws.requests import ExecuteActionRequest

from ._parser import update_event


def send_action_information(
    connection: Connection, manager: WebSocketManager, event: Event, executed: bool
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[bool](
                ok=True,
                result=executed,
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        ),
    )


async def execute_action_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=ExecuteActionRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    if not poker.started or poker.engine.round.showdown:
        return send_action_information(
            connection=connection, manager=manager, event=event, executed=False
        )

    poker.execute(
        action=PlayerAction(
            event.request.action.amount,
            ActionE(event.request.action.action),
            PositionE(event.request.action.position),
        )
    )
    await save(redis=redis, key=event.request.poker, value=poker)

    send_action_information(connection=connection, manager=manager, event=event, executed=True)

    return None
