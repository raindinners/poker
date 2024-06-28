from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import BONUS_AMOUNT, BalanceModel


async def create_balance(session: AsyncSession, user_id: int) -> None:
    await session.execute(insert(BalanceModel).values({BalanceModel.user_id: user_id}))


async def get_balance_by_id(session: AsyncSession, balance_id: int) -> Optional[BalanceModel]:
    result = await session.execute(
        select(BalanceModel)
        .where(BalanceModel.id == balance_id)
        .options(joinedload(BalanceModel.user))
    )

    return result.scalars().one_or_none()


async def take_bonus(
    session: AsyncSession,
    balance_id: int,
    bonus_increment_time_hours: int,
    bonus_amount: int = BONUS_AMOUNT,
) -> None:
    await session.execute(
        update(BalanceModel)
        .where(BalanceModel.id == balance_id)
        .values(
            {
                BalanceModel.balance: BalanceModel.balance + bonus_amount,
                BalanceModel.last_time_claimed_bonus: datetime.datetime.now()
                + datetime.timedelta(hours=bonus_increment_time_hours),
            }
        )
    )
