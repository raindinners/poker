from __future__ import annotations

from typing import Final, Type, Union

from pokerengine.engine import EngineRake01

URANDOM_SIZE: Final[int] = 64
"""Using in function: `os.random` as `__size` argument."""

ENGINE_CLASS: Type[Union[EngineRake01]] = EngineRake01
"""Engine base class."""

START_TIME: Final[int] = 15
"""Start game after time (in seconds)."""

AUTO_ACTION_TIME: Final[int] = 10
"""Time to wait until player did a move (in seconds)."""
