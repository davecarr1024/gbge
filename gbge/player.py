from abc import ABC, abstractmethod
from dataclasses import dataclass


class Player(ABC):
    @abstractmethod
    def move(self, board: "board.Board") -> "board.Board":
        ...


@dataclass(frozen=True)
class SearchPlayer(Player):
    search: "board.Board.Search"

    def move(self, board: "board.Board") -> "board.Board":
        return self.search(board, self).board


from gbge import board
