from __future__ import annotations

from typing import Protocol, Type, TypeVar

from redis.asyncio import Redis


class RedisSupportable(Protocol):
    def _encode(self) -> str:
        ...

    @classmethod
    def _decode(cls, from_: str) -> RedisSupportable:
        ...


ClassType = TypeVar("ClassType", bound=RedisSupportable)


async def save(redis: Redis, key: str, value: ClassType) -> None:
    await redis.set(name=key, value=value._encode())  # noqa


async def load(redis: Redis, key: str, type: Type[ClassType]) -> ClassType:
    return type._decode(await redis.get(name=key))  # noqa
