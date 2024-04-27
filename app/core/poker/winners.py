from __future__ import annotations

from typing import List, Tuple, Union

from distributed_websocket import Message, WebSocketManager

from enums import AutoEvent
from logger import logger
from poker import Poker
from schemas import ApplicationResponse
from utils.poker import get_entire_player_ids


def get_response(poker: Poker) -> Union[List[Tuple[str, int]], List[int]]:
    return (
        [(str(result), stack) for result, stack in poker.engine.pot.pay(cards=poker.cards)]
        if poker.engine.positions.showdown
        else poker.engine.pot.pay_noshowdown()
    )


def send_winners(manager: WebSocketManager, poker: Poker) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Union[List[Tuple[str, int]], List[int]]](
                ok=True,
                result=get_response(poker=poker),
                event_type=AutoEvent.WINNERS,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


async def winners(manager: WebSocketManager, poker: Poker) -> None:
    if not poker.started or not poker.engine.round.terminal_state:
        return logger.debug("Skipping winners: wrong state")

    send_winners(manager=manager, poker=poker)
    poker.is_winners = False
    poker.started = False

    return None
