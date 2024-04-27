from __future__ import annotations


class ApplicationError(Exception):
    ...


class PokerError(ApplicationError):
    ...


class PlayerLeftError(PokerError):
    ...
