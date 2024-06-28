from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .orm_schema import ORMSchema

if TYPE_CHECKING:
    from .balance import Balance


class User(ORMSchema):
    balance: Optional[Balance] = None
