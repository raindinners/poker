from __future__ import annotations

from distributed_websocket import Connection, Message, WebSocketManager
from pokerengine.engine import Player as PPlayer
from redis.asyncio import Redis

from _redis import save
from orm import BalanceModel
from orm.core import async_sessionmaker
from poker import Poker
from schemas import ApplicationResponse, Event, Player
from store import change_balance_for_user
from utils.poker import get_entire_player_ids, get_player_by_id, get_poker
from ws.requests import ExitRequest

from ._parser import update_event


def remove_player(poker: Poker, player: PPlayer) -> None:
    poker.engine.players.remove_player(id=player.id)


def send_player_left(
    manager: WebSocketManager, poker: Poker, player: PPlayer, event: Event
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Player](
                ok=True,
                result=Player.model_validate(player),
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


async def change_balance(user_id: int, stack: int) -> None:
    async with async_sessionmaker.begin() as session:
        await change_balance_for_user(
            session=session,
            user_id=user_id,
            values={BalanceModel.balance: BalanceModel.balance + stack},
        )


async def exit_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=ExitRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    player = get_player_by_id(poker=poker, id_=connection.id)
    if not poker.started:
        await change_balance(user_id=int(player.id), stack=player.stack)

    remove_player(poker=poker, player=player)
    await save(redis=redis, key=event.request.poker, value=poker)

    send_player_left(manager=manager, poker=poker, player=player, event=event)
