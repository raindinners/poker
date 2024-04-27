from __future__ import annotations

from typing import Optional

from pokerengine.card import CardGenerator
from pokerengine.card import Cards as PCards
from pokerengine.constants import BOARD_SIZE, HAND_SIZE
from pokerengine.engine import EngineTraits
from pokerengine.engine import Player as PPlayer
from pokerengine.engine import PlayerAction
from pokerengine.enums import PositionE, RoundE, StateE

from metadata import ENGINE_CLASS
from schemas import Card, Cards, Hand, Player, PokerRedis, Traits


class Poker:
    def __init__(
        self,
        traits: EngineTraits,
        *,
        auto_action_time: Optional[float] = None,
        seed: int = 1927,
        started: bool = False,
        start_at: Optional[float] = None,
        is_winners: bool = False,
        cards: Optional[PCards] = None,
    ) -> None:
        self.started: bool = started
        self.start_at: Optional[float] = start_at

        self.is_winners: bool = is_winners

        self.cards: Optional[PCards] = cards

        self.seed = seed
        self.cards_generator = CardGenerator(seed=self.seed)
        self.auto_action_time: Optional[float] = auto_action_time

        self.engine = ENGINE_CLASS(traits=traits)

    def start(self) -> None:
        self.started = True
        self.start_at = None
        self.is_winners = False
        self.engine.start(new_game=bool(self.cards))
        self.cards = PCards(
            cards=self.cards_generator.generate_v(
                BOARD_SIZE + len(self.engine.players.players) * HAND_SIZE
            )
        )

    def stop(self) -> None:
        self.started = False
        self.start_at = None
        self.is_winners = False
        self.engine.stop()

    def execute(self, action: PlayerAction) -> None:
        self.engine.actions.execute(action=action)
        self.auto_action_time = None

    def _encode(self) -> str:
        return PokerRedis(
            traits=Traits.model_validate(self.engine.traits),
            players=[Player.model_validate(player) for player in self.engine.players.players],
            position=self.engine.positions.current,
            round=self.engine.round.round,
            flop_dealt=self.engine.round.flop_dealt,
            seed=self.seed,
            started=self.started,
            start_at=self.start_at,
            is_winners=self.is_winners,
            auto_action_time=self.auto_action_time,
            cards=Cards(
                board=[Card(value=card.card, string=str(card)) for card in self.cards.board],
                hands=[
                    Hand(
                        front=Card(value=hand.value[0].card, string=str(hand.value[0])),
                        back=Card(value=hand.value[1].card, string=str(hand.value[1])),
                    )
                    for hand in self.cards.hands
                ],
            )
            if self.cards
            else None,
        ).model_dump_json()

    @classmethod
    def _decode(cls, value: str) -> Poker:
        encoded = PokerRedis.parse_raw(value)

        poker = cls(
            traits=EngineTraits(
                sb_bet=encoded.traits.sb_bet,
                bb_bet=encoded.traits.bb_bet,
                bb_mult=encoded.traits.bb_mult,
                min_raise=encoded.traits.min_raise,
            ),
            auto_action_time=encoded.auto_action_time,
            seed=encoded.seed,
            started=encoded.started,
            start_at=encoded.start_at,
            is_winners=encoded.is_winners,
            cards=PCards(
                board=[card.string for card in encoded.cards.board],
                hands=[hand.front.string + hand.back.string for hand in encoded.cards.hands],
            )
            if encoded.cards
            else None,
        )
        poker.engine.load(
            traits=EngineTraits(
                sb_bet=encoded.traits.sb_bet,
                bb_bet=encoded.traits.bb_bet,
                bb_mult=encoded.traits.bb_mult,
                min_raise=encoded.traits.min_raise,
            ),
            players=[
                PPlayer(
                    is_left=player.is_left,
                    stack=player.stack,
                    behind=player.behind,
                    front=player.front,
                    round_bet=player.round_bet,
                    state=StateE(player.state),
                    id=player.id,
                )
                for player in encoded.players
            ],
            position=PositionE(encoded.position),
            round=RoundE(encoded.round),
            flop_dealt=encoded.flop_dealt,
        )

        return poker
