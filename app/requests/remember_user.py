from __future__ import annotations

from schemas import ApplicationSchema


class RememberUserRequest(ApplicationSchema):
    user_id: int
