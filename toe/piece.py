from dataclasses import dataclass
from gbge.board import grid


@dataclass(frozen=True)
class Piece(grid.Piece["player.Player"]):
    ...


from toe import player
