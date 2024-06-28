from __future__ import annotations

from distributed_websocket import Connection, Message, WebSocketManager
from redis.asyncio import Redis

from _redis import save
from orm import BalanceModel
from orm.core import async_sessionmaker
from poker import Poker
from schemas import ApplicationResponse, Event, Player
from store import change_balance_for_user, get_balance_by_user_id
from utils.poker import get_entire_player_ids, get_player_by_id, get_poker
from ws.requests import JoinRequest

from ._parser import update_event


def add_player(poker: Poker, stack: int, id_: str) -> None:
    poker.engine.players.add_player(stack=stack, id=id_)
    if not poker.started:
        poker.start_at = None


def send_player_joined(
    connection: Connection, manager: WebSocketManager, poker: Poker, event: Event
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Player](
                ok=True,
                result=Player.model_validate(get_player_by_id(poker=poker, id_=connection.id)),
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


def send_join_error(connection: Connection, manager: WebSocketManager, event: Event) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Player](
                ok=False,
                result=False,
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        )
    )


async def change_balance(poker: Poker, user_id: int) -> bool:
    stack = poker.engine.traits.bb_bet * poker.engine.traits.bb_mult

    async with async_sessionmaker.begin() as session:
        balance = await get_balance_by_user_id(session=session, user_id=user_id)
        if balance.balance < stack:
            return False

        await change_balance_for_user(
            session=session,
            user_id=user_id,
            values={BalanceModel.balance: BalanceModel.balance - stack},
        )

    return True


async def join_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=JoinRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    if not await change_balance(poker=poker, user_id=int(connection.id)):
        send_join_error(connection=connection, manager=manager, event=event)
        return

    add_player(poker=poker, stack=event.request.stack, id_=connection.id)
    await save(redis=redis, key=event.request.poker, value=poker)

    send_player_joined(connection=connection, manager=manager, poker=poker, event=event)
