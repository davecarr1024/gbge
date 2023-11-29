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


from toe import player
