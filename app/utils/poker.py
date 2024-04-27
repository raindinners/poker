from __future__ import annotations

from typing import List, Optional

from pokerengine.engine import Player
from pokerengine.enums import PositionE
from redis.asyncio import Redis

from _redis import load
from poker import Poker


async def get_poker(redis: Redis, poker: str) -> Poker:
    return await load(redis=redis, key=poker, type=Poker)


def get_entire_player_ids(poker: Poker) -> List[str]:
    return [player.id for player in poker.engine.players.players]


def get_player_by_id(poker: Poker, id_: str) -> Optional[Player]:
    for player in poker.engine.players.players:
        if player.id == id_:
            return player

    return None


def get_player_position(poker: Poker, player: Player) -> PositionE:
    position = PositionE.SB
    for _player in poker.engine.players.players:
        if player.id == _player.id:
            return position

        position = PositionE(position.value + 1)

    return PositionE.NONE
