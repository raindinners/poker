from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import ORMModel, types

if TYPE_CHECKING:
    from .user import UserModel

BALANCE_DEFAULT: Final[int] = 15000
BONUS_AMOUNT: Final[int] = 10000
BONUS_INCREMENT_TIME_HOURS: Final[int] = 4


class BalanceModel(ORMModel):
    balance: Mapped[types.BigInt] = mapped_column(default=BALANCE_DEFAULT)
    bonus_increment_time_hours: Mapped[types.BigInt] = mapped_column(
        default=BONUS_INCREMENT_TIME_HOURS
    )
    last_time_claimed_bonus: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    user_id: Mapped[types.UserID]
    user: Mapped[Optional[UserModel]] = relationship(back_populates="balance")
