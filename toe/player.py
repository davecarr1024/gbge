from dataclasses import dataclass
from gbge import sides
from toe import side


@dataclass(frozen=True)
class Player(
    sides.Player[
        "state.State",
        "board.Board",
        side.Side,
    ],
):
    ...


from toe import state, board
