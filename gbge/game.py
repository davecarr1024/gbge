from abc import ABC, abstractmethod
from typing import Sequence


class Game(ABC):
    class Result:
        ...

    @property
    @abstractmethod
    def players(self) -> Sequence["player.Player"]:
        ...

    def next_player(self, player: "player.Player") -> "player.Player":
        return self.players[(self.players.index(player) + 1) % len(self.players)]

    @property
    @abstractmethod
    def initial_board(self) -> "board.Board":
        ...


from gbge import board, player
