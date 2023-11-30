from dataclasses import dataclass
from typing import FrozenSet, MutableSet
from gbge.board import grid


@dataclass(frozen=True)
class Board(
    grid.Grid[
        "player.Player",
        "piece.Piece",
        "result.Result",
    ]
):
    @classmethod
    def dim(cls) -> "Board.Dim":
        return Board.Dim(3, 3)

    def moves(self, player: "player.Player") -> FrozenSet["Board"]:
        dim = self.dim()
        for row in range(dim.rows):
            for col in range(dim.cols):
                pos = grid.Pos(row, col)
                if pos not in self:
                    yield self.with_piece(piece.Piece(player, pos))

    @classmethod
    def load(cls, game: "game.Game", input: str) -> "Board":
        dim = cls.dim()
        lines = input.split("\n")
        assert len(lines) == dim.rows
        assert all(len(line) == dim.cols for line in lines)
        pieces: MutableSet[piece.Piece] = set()
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                if val != " ":
                    pieces.add(piece.Piece(game[side.Side(val)], grid.Pos(row, col)))
        return Board(frozenset(pieces))

    @property
    def result(self) -> "result.Result":
        raise NotImplementedError()


from toe import game, player, piece, side, result
