from __future__ import annotations

from .schema import ApplicationSchema


class Traits(ApplicationSchema):
    sb_bet: int
    bb_bet: int
    bb_mult: int
    min_raise: int
