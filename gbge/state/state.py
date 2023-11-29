from abc import ABC
from dataclasses import dataclass
from typing import Generic, Self, TypeVar

_Game = TypeVar("_Game", bound="game.Game")
_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class State(
    ABC,
    Generic[_Game, _Board, _Player],
):
    game: _Game
    board: _Board
    player: _Player

    def move(self) -> Self:
        return self.__class__(
            self.game,
            self.player.move(self),
            self.game.next_player(self.player),
        )


from gbge.game import game
from gbge.board import board
from gbge.player import player
