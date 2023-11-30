from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

_Game = TypeVar("_Game", bound="game.Game")
_Board = TypeVar("_Board", bound="board.Board")


@dataclass(frozen=True)
class Player(
    ABC,
    Generic[
        _Game,
        _Board,
    ],
):
    @abstractmethod
    def move(self, board: _Board) -> _Board:
        ...


from gbge import game, board
