from __future__ import annotations

from schemas import Action, ApplicationSchema


class ExecuteActionRequest(ApplicationSchema):
    poker: str
    action: Action
