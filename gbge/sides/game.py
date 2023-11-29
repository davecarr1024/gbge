from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, Mapping, Type, TypeVar
from gbge.game import game

_Player = TypeVar("_Player", bound="player.Player")
_Side = TypeVar("_Side", bound=StrEnum)


@dataclass(frozen=True)
class Game(
    Generic[_Player, _Side],
    game.Game[_Player],
    Mapping[_Side, _Player],
):
    _side: Type[_Side]
    _players: Mapping[_Side, _Player]

    def __post_init__(self) -> None:
        if not len(self._players) == len(self._side):
            raise ValueError(self._players)

    def next_player(self, player: _Player) -> _Player:
        raise NotImplementedError(self, player)


from gbge.sides import player
