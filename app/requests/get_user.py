from __future__ import annotations

from schemas import ApplicationSchema


class GetUserRequest(ApplicationSchema):
    user_id: int
