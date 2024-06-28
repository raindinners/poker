from __future__ import annotations

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from core.settings import api_protect_settings, server_settings


def api_protect(request: Request) -> None:
    if (
        not server_settings.DEBUG
        and request.client.host not in api_protect_settings.ALLOWED_IPS.split()
    ):
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
