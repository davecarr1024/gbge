from dataclasses import dataclass
import gbge


@dataclass(frozen=True)
class Piece(gbge.grid.Piece["player.Player"]):
    ...


from toe import player
