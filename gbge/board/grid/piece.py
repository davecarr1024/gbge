from dataclasses import dataclass
from typing import Generic, TypeVar
from . import pos

_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Piece(
    Generic[_Player],
):
    player: _Player
    pos: pos.Pos

    def __str__(self) -> str:
        return str(self.player)


from gbge.player import player
