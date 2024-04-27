from __future__ import annotations

from schemas import ApplicationSchema


class ExitRequest(ApplicationSchema):
    poker: str
