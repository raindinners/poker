from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import ORMModel, types

if TYPE_CHECKING:
    from .balance import BalanceModel


class UserModel(ORMModel):
    id: Mapped[types.BigInt] = mapped_column(primary_key=True, unique=True)

    balance: Mapped[Optional[BalanceModel]] = relationship(back_populates="user")
