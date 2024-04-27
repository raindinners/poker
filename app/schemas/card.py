from __future__ import annotations

from typing import List

from .schema import ApplicationSchema


class Card(ApplicationSchema):
    value: int
    string: str


class Hand(ApplicationSchema):
    front: Card
    back: Card


class Cards(ApplicationSchema):
    board: List[Card]
    hands: List[Hand]


class PokerCards(ApplicationSchema):
    board: List[Card]
    hand: Hand
