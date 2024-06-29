from __future__ import annotations

from enum import Enum


class State(str, Enum):
    STARTING = "STARTING"
    STOPPED = "STOPPED"
    STARTED = "STARTED"
    ACTIONS = "ACTIONS"
    AUTO = "AUTO"
