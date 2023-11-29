from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar
from gbge.player import player

_State = TypeVar("_State", bound="state.State")
_Board = TypeVar("_Board", bound="board.Board")
_Side = TypeVar("_Side", bound=StrEnum)


@dataclass(frozen=True)
class Player(
    Generic[_State, _Board, _Side],
    player.Player[_State, _Board],
):
    side: _Side

    def __str__(self) -> str:
        return str(self.side)


from gbge.state import state
from gbge.board import board
