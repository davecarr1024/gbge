from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, Iterator, Mapping, Type, TypeVar
from gbge.game import game

_Player = TypeVar("_Player", bound="player.Player")
_Side = TypeVar("_Side", bound=StrEnum)


@dataclass(frozen=True)
class Game(
    Generic[_Player, _Side],
    game.Game[_Player],
    Mapping[_Side, _Player],
):
    _side_type: Type[_Side]
    _players: Mapping[_Side, _Player]

    def __post_init__(self) -> None:
        if not len(self._players) == len(self._side_type):
            raise ValueError(self._players)

    def next_player(self, player: _Player) -> _Player:
        raise NotImplementedError(self, player)

    def __len__(self) -> int:
        return len(self._players)

    def __iter__(self) -> Iterator[_Side]:
        return iter(self._players)

    def __getitem__(self, side: _Side) -> _Player:
        return self._players[side]


from gbge.sides import player
