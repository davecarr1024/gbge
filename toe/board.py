from dataclasses import dataclass, field
from typing import Iterable
from gbge.board import grid


@dataclass(frozen=True)
class Board(grid.Grid["player.Player", "piece.Piece"]):
    rows: int = field(init=False, default=3)
    cols: int = field(init=False, default=3)

    def moves(self, player: "player.Player") -> Iterable["Board"]:
        raise NotImplementedError(self, player)


from toe import player, piece
