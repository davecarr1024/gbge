from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, Self, TypeVar


_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Board(
    ABC,
    Generic[_Player],
):
    @abstractmethod
    def moves(self, player: _Player) -> Iterable[Self]:
        ...


from gbge.player import player
