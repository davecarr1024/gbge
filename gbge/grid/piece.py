from dataclasses import dataclass
from typing import Generic, Self, TypeVar
from gbge.grid import pos as pos_lib

_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Piece(
    Generic[_Player],
):
    player: _Player
    pos: pos_lib.Pos

    def __str__(self) -> str:
        return str(self.player)

    def at_pos(self, pos: pos_lib.Pos) -> Self:
        return self.__class__(self.player, pos)


from gbge import player
