from dataclasses import dataclass
from gbge.board import grid
from toe import board, piece, player, state


@dataclass(frozen=True)
class TextPlayer(player.Player):
    def move(self, state: state.State) -> board.Board:
        while True:
            try:
                print(state.board)
                row = int(input("row> "))
                col = int(input("col> "))
                return state.board.with_piece(piece.Piece(self, grid.Pos(row, col)))
            except Exception as error:
                print(error)
