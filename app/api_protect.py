from __future__ import annotations

from functools import lru_cache
from typing import Final, List

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from core.settings import api_protect_settings, server_settings

_IPS: Final[List[str]] = api_protect_settings.ALLOWED_IPS.split()


@lru_cache()
def is_allowed(host: str) -> bool:
    return host in _IPS


def api_protect(request: Request) -> None:
    if not server_settings.DEBUG and is_allowed(request.client.host):
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
