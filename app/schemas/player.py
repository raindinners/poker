from __future__ import annotations

from pokerengine.enums import StateE

from .schema import ApplicationSchema, ToJSON


class Player(ApplicationSchema):
    id: str
    is_left: bool
    stack: int
    behind: int
    front: int
    round_bet: int
    state: ToJSON[StateE]
