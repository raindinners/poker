from __future__ import annotations

from schemas import ApplicationSchema


class CreateRequest(ApplicationSchema):
    sb_bet: int
    bb_bet: int
    bb_mult: int
    min_raise: int = -1
