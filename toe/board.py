from dataclasses import dataclass
from typing import FrozenSet, MutableSet, Optional
import gbge


@dataclass(frozen=True)
class Board(
    gbge.sides_grid.Board[
        "game.Game",
        "player.Player",
        "piece.Piece",
        "result.Result",
        "side.Side",
    ]
):
    @classmethod
    def dim(cls) -> gbge.grid.Dim:
        return gbge.grid.Dim(3, 3)

    @classmethod
    def piece(cls, player: "player.Player", pos: gbge.grid.Pos) -> "piece.Piece":
        return piece.Piece(player, pos)

    def moves(self, player: "player.Player") -> FrozenSet["Board"]:
        dim = self.dim()
        boards: MutableSet[Board] = set()
        for row in range(dim.rows):
            for col in range(dim.cols):
                pos = gbge.grid.Pos(row, col)
                if pos not in self:
                    boards.add(self | self.piece(player, pos))
        return frozenset(boards)

    def result(self) -> Optional["result.Result"]:
        dim = self.dim()

        def at(row, col) -> Optional[player.Player]:
            return self[row, col].player if (row, col) in self else None

        if len(self) == dim.rows * dim.cols:
            return result.Result(side.Side.x, result.Result.Type.tie)

        for player_ in self.game.players:
            for row in range(dim.rows):
                if all(at(row, col) == player_ for col in range(dim.cols)):
                    return result.Result(player_.side)
            for col in range(dim.cols):
                if all(at(row, col) == player_ for row in range(dim.rows)):
                    return result.Result(player_.side)
            if dim.rows == dim.cols:
                if all(at(i, i) == player_ for i in range(dim.rows)):
                    return result.Result(player_.side)
                if all(at(dim.rows - 1 - i, i) == player_ for i in range(dim.rows)):
                    return result.Result(player_.side)
        return None


from toe import game, player, piece, result, side
