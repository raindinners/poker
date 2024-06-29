from __future__ import annotations

from enum import Enum


class AutoEvent(str, Enum):
    ACTIONS = "ACTIONS"
    INFORMATION = "INFORMATION"
    START = "START"
    WINNERS = "WINNERS"
