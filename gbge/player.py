from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

_Board = TypeVar("_Board", bound="board.Board")


@dataclass(frozen=True)
class Player(ABC, Generic[_Board]):
    @abstractmethod
    def move(self, board: _Board) -> _Board:
        ...


from gbge.board import board
