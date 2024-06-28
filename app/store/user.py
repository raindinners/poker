from __future__ import annotations

from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import UserModel


async def create_user(session: AsyncSession, user_id: int) -> None:
    await session.execute(insert(UserModel).values({UserModel.id: user_id}))


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[UserModel]:
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id).options(joinedload(UserModel.balance))
    )

    return result.scalars().one_or_none()
