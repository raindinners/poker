from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from metadata import BALANCE_DEFAULT, BONUS_INCREMENT_TIME_HOURS

from .core import ORMModel, types

if TYPE_CHECKING:
    from .user import UserModel


class BalanceModel(ORMModel):
    balance: Mapped[types.BigInt] = mapped_column(default=BALANCE_DEFAULT)
    bonus_increment_time_hours: Mapped[types.BigInt] = mapped_column(
        default=BONUS_INCREMENT_TIME_HOURS
    )
    last_time_claimed_bonus: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    user_id: Mapped[types.UserID]
    user: Mapped[Optional[UserModel]] = relationship(back_populates="balance")
