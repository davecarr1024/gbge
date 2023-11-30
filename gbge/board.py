from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, Generic, Optional, Self, TypeVar

_Game = TypeVar("_Game", bound="game.Game")
_Player = TypeVar("_Player", bound="player.Player")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Board(
    ABC,
    Generic[
        _Game,
        _Player,
        _Result,
    ],
):
    @abstractmethod
    def moves(self, player: _Player) -> FrozenSet[Self]:
        ...

    @abstractmethod
    def result(self) -> Optional[_Result]:
        ...


from gbge import game, player
