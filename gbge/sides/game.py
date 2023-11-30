from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Generic, Iterator, Mapping, Type, TypeVar
from gbge import game

_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")
_Result = TypeVar("_Result", bound="result.Result")
_Side = TypeVar("_Side", bound=Enum)


@dataclass(frozen=True)
class Game(
    Generic[_Board, _Player, _Result, _Side],
    game.Game[_Board, _Player, _Result],
    Mapping[_Side, _Player],
):
    _side_type: Type[_Side]

    @cached_property
    def players_by_side(self) -> Mapping[_Side, _Player]:
        return {player.side: player for player in self.players}

    def __post_init__(self) -> None:
        assert len(self.players_by_side) == len(self.players), "duplicate player sides"
        assert len(self.players_by_side) == len(self._side_type), "missing player sides"

    def __len__(self) -> int:
        return len(self.players_by_side)

    def __iter__(self) -> Iterator[_Side]:
        return iter(self.players_by_side)

    def __getitem__(self, side: _Side) -> _Player:
        return self.players_by_side[side]


from gbge.sides import player, result
from gbge import board
