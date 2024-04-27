from __future__ import annotations

from typing import Annotated, Any, Generic, Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict, PlainSerializer

from enums import AutoEvent, EventType

PokerType = TypeVar("PokerType", bound=Any)
ToJSON = Annotated[Union[PokerType, int], PlainSerializer(lambda x: x.value)]


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True,
    )


class ApplicationSchema(_BaseModel):
    ...


class ApplicationResponse(_BaseModel, Generic[PokerType]):
    ok: bool
    result: Optional[PokerType] = None
    event_type: Optional[Union[AutoEvent, EventType]] = None
    detail: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[int] = None
