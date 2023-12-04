from dataclasses import dataclass
from typing import Generic, TypeVar
from gbge.board.enumerator import enumerator, result

_Game = TypeVar("_Game", bound="game.Game")
_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")


@dataclass(frozen=True)
class Full(
    Generic[_Game, _Board, _Player],
    enumerator.Enumerator[_Board, _Player],
):
    game: _Game

    def __call__(self, board: _Board, player: _Player) -> result.Result[_Board]:
        next_player = self.game.next_player(player)
        return result.Result[_Board](
            board, [self(child, next_player) for child in board.moves(player)]
        )


from gbge.board import board
from gbge import game, player
