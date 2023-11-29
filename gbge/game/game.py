from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Game(
    ABC,
    Generic[_Player],
):
    @abstractmethod
    def next_player(self, player: _Player) -> _Player:
        ...


from gbge.player import player
