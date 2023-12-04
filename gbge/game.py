from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar


_Board = TypeVar("_Board", bound="board.Board")
_Player = TypeVar("_Player", bound="player.Player")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Game(ABC, Generic[_Board, _Player, _Result]):
    @property
    @abstractmethod
    def initial_board(self) -> _Board:
        ...

    @property
    @abstractmethod
    def players(self) -> Sequence[_Player]:
        ...

    def next_player(self, player: _Player) -> _Player:
        players = self.players
        return players[(players.index(player) + 1) % len(players)]

    def run(self) -> _Result:
        board = self.initial_board
        player = self.players[0]
        while board.result is None:
            board = player.move(board)
            player = self.next_player(player)
        return board.result


from gbge import player
from gbge.board import board
