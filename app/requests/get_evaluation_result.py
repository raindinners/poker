from __future__ import annotations

from typing import List

from schemas import ApplicationSchema


class GetEvaluationResultRequest(ApplicationSchema):
    board: List[str]
    hands: List[str]
    players: List[int]
