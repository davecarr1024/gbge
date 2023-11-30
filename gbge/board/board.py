from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, Generic, Self, TypeVar


_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Board(
    ABC,
    Generic[_Player],
):
    @abstractmethod
    def moves(self, player: _Player) -> FrozenSet[Self]:
        ...


from gbge.player import player
