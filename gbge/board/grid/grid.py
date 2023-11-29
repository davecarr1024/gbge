from dataclasses import dataclass, field
from typing import Generic, Iterator, Mapping, MutableMapping, Self, TypeVar
from gbge.board import board
from gbge.board.grid import pos

_Player = TypeVar("_Player", bound="player.Player")
_Piece = TypeVar("_Piece", bound="piece.Piece")


@dataclass(frozen=True)
class Grid(
    Generic[_Player, _Piece],
    board.Board[_Player],
    Mapping[pos.Pos, _Piece],
):
    rows: int
    cols: int
    _pieces: Mapping[pos.Pos, _Piece] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for pos_, piece in self._pieces.items():
            if (
                pos_ != piece.pos
                or pos_.row < 0
                or pos_.row >= self.rows
                or pos_.col < 0
                or pos_.col >= self.cols
            ):
                raise ValueError(pos_, piece)

    def __str__(self) -> str:
        s = ""
        for col in range(self.cols):
            s += "+-"
        s += "+\n"
        for row in range(self.rows):
            for col in range(self.cols):
                s += "|"
                pos_ = pos.Pos(row, col)
                if pos_ in self._pieces:
                    s += str(self._pieces[pos_])
                else:
                    s += " "
            s += "|\n"
            for col in range(self.cols):
                s += "+-"
            s += "+\n"
        return s

    def __len__(self) -> int:
        return len(self._pieces)

    def __iter__(self) -> Iterator[pos.Pos]:
        return iter(self._pieces)

    def __getitem__(self, key: pos.Pos | tuple[int, int]) -> _Piece:
        match key:
            case pos.Pos():
                return self._pieces[key]
            case row, col:
                return self._pieces[pos.Pos(row, col)]
            case _:
                raise TypeError(key)

    def _with_pieces(self, pieces: Mapping[pos.Pos, _Piece]) -> Self:
        return self.__class__(self.rows, self.cols, pieces)

    def with_piece(self, piece: _Piece) -> Self:
        return self._with_pieces(dict(self._pieces) | {piece.pos: piece})

    def without_piece(self, piece: _Piece) -> Self:
        pieces: MutableMapping[pos.Pos, _Piece] = dict(self._pieces)
        if piece.pos in pieces:
            pieces.pop(piece.pos)
        return self._with_pieces(pieces)


from gbge.player import player
from gbge.board.grid import piece
