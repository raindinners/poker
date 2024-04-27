from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pokerengine.enums import PositionE, RoundE

from .schema import ApplicationSchema, ToJSON

if TYPE_CHECKING:
    from .card import Cards
    from .player import Player
    from .traits import Traits


class PokerRedis(ApplicationSchema):
    traits: Traits
    players: List[Player]
    position: ToJSON[PositionE]
    round: ToJSON[RoundE]
    flop_dealt: bool
    seed: int
    started: bool
    start_at: Optional[float]
    is_winners: bool
    auto_action_time: Optional[float]
    cards: Optional[Cards]
