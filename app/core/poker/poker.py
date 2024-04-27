from __future__ import annotations

from distributed_websocket import WebSocketManager
from redis.asyncio import Redis

from _redis import save
from logger import logger
from poker import Poker
from utils.poker import get_poker

from .actions import actions
from .information import information
from .start import start
from .winners import winners


async def core(manager: WebSocketManager, poker: Poker) -> None:
    await winners(manager=manager, poker=poker)
    await start(manager=manager, poker=poker)
    await actions(manager=manager, poker=poker)
    await information(manager=manager, poker=poker)


async def game(manager: WebSocketManager, redis: Redis, poker: str) -> None:
    _poker = await get_poker(redis=redis, poker=poker)

    try:
        await core(manager=manager, poker=_poker)
    except Exception as exc:
        logger.exception(exc)

    await save(redis=redis, key=poker, value=_poker)
