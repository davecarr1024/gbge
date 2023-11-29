from dataclasses import dataclass, field
from typing import Iterable, MutableMapping
from gbge.board import grid


@dataclass(frozen=True)
class Board(grid.Grid["player.Player", "piece.Piece"]):
    @classmethod
    def dim(cls) -> "Board.Dim":
        return Board.Dim(3, 3)

    def moves(self, player: "player.Player") -> Iterable["Board"]:
        for row in range(self.dim().rows):
            for col in range(self.dim().cols):
                pos = grid.Pos(row, col)
                if pos not in self:
                    yield self.with_piece(piece.Piece(player, pos))

    @classmethod
    def load(cls, game: "game.Game", input: str) -> "Board":
        dim = cls.dim()
        lines = input.split("\n")
        assert len(lines) == dim.rows
        assert all(len(line) == dim.cols for line in lines)
        pieces: MutableMapping[grid.Pos, piece.Piece] = {}
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                if val != " ":
                    pos = grid.Pos(row, col)
                    pieces[pos] = piece.Piece(game[side.Side(val)], pos)
        return Board(pieces)


from toe import game, player, piece, side
