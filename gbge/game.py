from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, Sequence, TypeVar

_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Game(
    ABC,
    Generic[
        _Board,
        _Player,
        _Result,
    ],
):
    players: Sequence[_Player]

    @abstractmethod
    def initial_board(self) -> _Board:
        ...

    def next_player(self, player: _Player) -> _Player:
        return self.players[(self.players.index(player) + 1) % len(self.players)]

    def run(self, board: _Board) -> _Result:
        result: Optional[_Result] = board.result()
        player = self.players[0]
        while result is None:
            next_board = player.move(board)
            assert next_board in board.moves(player), "invalid move"
            board = next_board
            player = self.next_player(player)
            result = board.result()
        return result


from gbge import board, player
