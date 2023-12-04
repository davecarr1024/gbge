from dataclasses import dataclass, field
from typing import Type
import gbge


@dataclass(frozen=True)
class Game(
    gbge.sides.Game[
        "board.Board",
        "player.Player",
        "result.Result",
        "side.Side",
    ]
):
    _side_type: Type["side.Side"] = field(
        default_factory=lambda: side.Side,
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )

    def initial_board(self) -> "board.Board":
        return board.Board(self)

    @property
    def x(self) -> "player.Player":
        return self[side.Side.x]

    @property
    def o(self) -> "player.Player":
        return self[side.Side.o]


from toe import board, player, result, side
