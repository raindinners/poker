from __future__ import annotations

from schemas import ApplicationSchema


class JoinRequest(ApplicationSchema):
    poker: str
