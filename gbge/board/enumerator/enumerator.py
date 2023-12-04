from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, TypeVar
from gbge.board.enumerator import result

_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Enumerator(ABC, Generic[_Board, _Player]):
    @abstractmethod
    def __call__(self, board: _Board, player: _Player) -> result.Result[_Board]:
        ...


from gbge.board import board
from gbge import player
