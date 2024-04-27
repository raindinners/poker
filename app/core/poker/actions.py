from __future__ import annotations

import time
from typing import List, Optional

from distributed_websocket import Message, WebSocketManager
from pokerengine.engine import PlayerAction
from pokerengine.enums import ActionE, PositionE

from enums import AutoEvent, State
from logger import logger
from metadata import AUTO_ACTION_TIME
from poker import Poker
from schemas import Action, ApplicationResponse, ApplicationSchema
from utils.poker import get_entire_player_ids


class ActionResponse(ApplicationSchema):
    state: State
    auto: Action
    time: Optional[float] = None
    actions: Optional[List[Action]] = None


def find_check_or_fold(actions: List[PlayerAction]) -> PlayerAction:
    for action in actions:
        if action.action == ActionE.CHECK:
            return action
        if action.action == ActionE.FOLD:
            return action

    return PlayerAction(amount=0, action=ActionE.NONE, position=PositionE.NONE)


def send_player_actions(manager: WebSocketManager, poker: Poker, auto: PlayerAction) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[ActionResponse](
                ok=True,
                result=ActionResponse(
                    state=State.ACTIONS,
                    auto=Action.model_validate(auto),
                    time=poker.auto_action_time,
                    actions=[
                        Action.model_validate(action) for action in poker.engine.actions.actions
                    ],
                ),
                event_type=AutoEvent.ACTIONS,
            ).model_dump(),
            typ="json",
            conn_id=poker.engine.positions.player.id,
        )
    )


def send_action_executed(manager: WebSocketManager, poker: Poker, auto: PlayerAction) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[ActionResponse](
                ok=True,
                result=ActionResponse(
                    state=State.AUTO,
                    auto=Action.model_validate(auto),
                ),
                event_type=AutoEvent.ACTIONS,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


async def actions(manager: WebSocketManager, poker: Poker) -> None:
    if not poker.started or poker.engine.round.terminal_state:
        return logger.debug("Skipping auto action: wrong game state")

    action = find_check_or_fold(actions=poker.engine.actions.actions)

    if not poker.auto_action_time:
        poker.auto_action_time = time.time() + AUTO_ACTION_TIME

        send_player_actions(manager=manager, poker=poker, auto=action)

    if time.time() < poker.auto_action_time and not poker.engine.positions.player.is_left:
        return logger.debug("Skipping auto action: wrong time")

    poker.execute(action=action)
    send_action_executed(manager=manager, poker=poker, auto=action)

    return None
