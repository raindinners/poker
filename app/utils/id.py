from __future__ import annotations

import os

from metadata import URANDOM_SIZE


def generate_id() -> str:
    return os.urandom(URANDOM_SIZE).hex()
