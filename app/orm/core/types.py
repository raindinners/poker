from __future__ import annotations

from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated, Final

BigInt: int = Annotated[int, mapped_column(types.BIGINT)]

USER_TABLE_NAME: Final[str] = "users"
UserID: int = Annotated[int, mapped_column(ForeignKey(f"{USER_TABLE_NAME}.id"))]
