from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar
from gbge import player

_Board = TypeVar("_Board", bound="board.Board")
_Side = TypeVar("_Side", bound=Enum)


@dataclass(frozen=True)
class Player(
    Generic[_Board, _Side],
    player.Player[_Board],
):
    side: _Side


from gbge import board
