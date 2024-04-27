from __future__ import annotations

from pokerengine.enums import ActionE, PositionE

from .schema import ApplicationSchema, ToJSON


class Action(ApplicationSchema):
    amount: int
    action: ToJSON[ActionE]
    position: ToJSON[PositionE]
