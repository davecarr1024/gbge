from dataclasses import dataclass
import gbge


@dataclass(frozen=True)
class Player(
    gbge.sides.Player[
        "board.Board",
        "side.Side",
    ]
):
    ...


from toe import board, side
