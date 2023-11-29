from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

_State = TypeVar("_State", bound="state.State")
_Board = TypeVar("_Board", bound="board.Board")


@dataclass(frozen=True)
class Player(
    ABC,
    Generic[_State, _Board],
):
    @abstractmethod
    def move(self, state: _State) -> _Board:
        ...


from gbge.state import state
from gbge.board import board
