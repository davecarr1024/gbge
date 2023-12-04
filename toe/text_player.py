from dataclasses import dataclass
import gbge
from toe import board, piece, player


@dataclass(frozen=True)
class TextPlayer(player.Player):
    def move(self, board: board.Board) -> board.Board:
        while True:
            try:
                print(self)
                print(board)
                row = int(input("row?"))
                col = int(input("col?"))
                return board | piece.Piece(self, gbge.grid.Pos(row, col))
            except Exception as error:
                print(error)
