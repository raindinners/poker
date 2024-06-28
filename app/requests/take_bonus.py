from __future__ import annotations

from schemas import ApplicationSchema


class TakeBonusRequest(ApplicationSchema):
    user_id: int
