from dataclasses import dataclass, field
from typing import Mapping, Type
from gbge import sides
from toe import side


@dataclass(frozen=True)
class Game(
    sides.Game[
        "player.Player",
        side.Side,
    ],
):
    _side_type: Type[side.Side] = field(
        init=False,
        default=side.Side,
    )

    @property
    def x(self) -> "player.Player":
        return self._players[side.Side.x]

    @property
    def o(self) -> "player.Player":
        return self._players[side.Side.o]


from toe import player
