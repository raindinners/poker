from __future__ import annotations

import datetime
from typing import Optional

from .orm_schema import ORMSchema


class Balance(ORMSchema):
    balance: int
    bonus_increment_time_hours: int
    last_time_claimed_bonus: Optional[datetime.datetime]
