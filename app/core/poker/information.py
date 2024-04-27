from __future__ import annotations

from typing import List

from distributed_websocket import Message, WebSocketManager
from pokerengine.enums import PositionE, RoundE

from enums import AutoEvent
from logger import logger
from poker import Poker
from schemas import (
    ApplicationResponse,
    ApplicationSchema,
    Card,
    Hand,
    Player,
    PokerCards,
    ToJSON,
    Traits,
)


class Information(ApplicationSchema):
    traits: Traits
    round: ToJSON[RoundE]
    players: List[Player]
    current: ToJSON[PositionE]
    poker_cards: PokerCards
    flop_dealt: bool
    pot: int
    pot_rake: int


def send_game_information(manager: WebSocketManager, poker: Poker) -> None:
    for position, player in enumerate(poker.engine.players.players):
        manager.send_by_conn_id(
            message=Message(
                data=ApplicationResponse[Information](
                    ok=True,
                    result=Information(
                        traits=Traits.model_validate(poker.engine.traits),
                        round=poker.engine.round.round,
                        flop_dealt=poker.engine.round.flop_dealt,
                        players=[
                            Player.model_validate(player)
                            for player in poker.engine.players.players
                        ],
                        current=poker.engine.positions.current,
                        poker_cards=PokerCards(
                            board=[
                                Card(value=card.card, string=str(card))
                                for card in poker.cards.board[
                                    poker.engine.round.round.value + 2
                                    if poker.engine.round.round != RoundE.PREFLOP
                                    else RoundE.PREFLOP.value
                                ]
                            ],
                            hand=Hand(
                                front=Card(
                                    value=poker.cards.hands[position].value[0].card,
                                    string=str(poker.cards.hands[position].value[0]),
                                ),
                                back=Card(
                                    value=poker.cards.hands[position].value[1].card,
                                    string=str(poker.cards.hands[position].value[1]),
                                ),
                            ),
                        ),
                        pot=poker.engine.pot.pot(),
                        pot_rake=poker.engine.pot.pot_rake(),
                    ),
                    event_type=AutoEvent.INFORMATION,
                ).model_dump(),
                typ="json",
                conn_id=player.id,
            ),
        )


async def information(manager: WebSocketManager, poker: Poker) -> None:
    if not poker.started or poker.engine.round.terminal_state:
        return logger.debug("Skipping auto action: wrong game state")

    send_game_information(manager=manager, poker=poker)

    return None
