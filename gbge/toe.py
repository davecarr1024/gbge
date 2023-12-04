from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Sequence

from gbge import board, game, player


class Side(StrEnum):
    x = auto()
    o = auto()


@dataclass(frozen=True)
class Player(player.Player):
    side: Side

    def __str__(self) -> str:
        return str(self.side)


@dataclass(frozen=True)
class SearchPlayer(Player):
    search: "board.Board.Search"

    def move(self, board: board.Board) -> board.Board:
        return self.search(board, self).board


s = SearchPlayer(Side.x, board.Board.MinMax())


@dataclass(frozen=True)
class Game(game.Game):
    x: Player
    o: Player

    def __post_init__(self) -> None:
        assert self.x.side == Side.x
        assert self.o.side == Side.o

    @property
    def players(self) -> Sequence[Player]:
        return self.x, self.o


class Board(board.MoveEmptyGrid):
    @classmethod
    def dim(cls) -> "board.Grid.Dim":
        return board.Grid.Dim(3, 3)


g = Game()
b = Board()
s.move(b)
