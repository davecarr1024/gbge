from dataclasses import dataclass
from typing import Iterable
from unittest import TestCase
from gbge.board import grid
from gbge.game import game

from gbge.player import player
from gbge.state import state


@dataclass(frozen=True)
class _Game(game.Game["_Player"]):
    ...


@dataclass(frozen=True)
class _State(state.State["_Game", "_Board", "_Player"]):
    ...


@dataclass(frozen=True)
class _Player(player.Player["_State", "_Board"]):
    name: str

    def __post_init__(self) -> None:
        assert len(self.name) == 1, f"invalid name {self.name}"

    def __str__(self) -> str:
        return self.name

    def move(self, state: "_State") -> "_Board":
        raise NotImplementedError()


@dataclass(frozen=True)
class _Board(grid.Grid["_Player", "_Piece"]):
    def moves(self, player: "_Player") -> Iterable["_Board"]:
        raise NotImplementedError()


@dataclass(frozen=True)
class _Piece(grid.Piece["_Player"]):
    ...


class GridTest(TestCase):
    def test_init(self) -> None:
        _Board(3, 3)
        a = _Player("a")
        print(_Board(3, 3).with_piece(_Piece(a, grid.Pos(0, 1))))
