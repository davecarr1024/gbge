from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cache, cached_property
from typing import (
    FrozenSet,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    Self,
    Sized,
    TypeVar,
)
from gbge.board import board
from gbge.board.grid import pos

_Player = TypeVar("_Player", bound="player.Player")
_Piece = TypeVar("_Piece", bound="piece.Piece")


@dataclass(frozen=True)
class Grid(
    Generic[_Player, _Piece],
    board.Board[_Player],
    Sized,
    Iterable[_Piece],
):
    _pieces: FrozenSet[_Piece] = field(default_factory=frozenset)

    @dataclass(frozen=True)
    class Dim:
        rows: int
        cols: int

    @classmethod
    @abstractmethod
    def dim(self) -> Dim:
        ...

    @cached_property
    def pieces_by_pos(self) -> Mapping[pos.Pos, _Piece]:
        return {piece.pos: piece for piece in self}

    def __post_init__(self) -> None:
        assert len(self.pieces_by_pos) == len(self._pieces), "duplicate piece pos"
        for piece in self._pieces:
            if (
                piece.pos.row < 0
                or piece.pos.row >= self.dim().rows
                or piece.pos.col < 0
                or piece.pos.col >= self.dim().cols
            ):
                raise ValueError(piece.pos, piece)

    def __str__(self) -> str:
        dim = self.dim()
        s = ""
        for col in range(dim.cols):
            s += "+-"
        s += "+\n"
        for row in range(dim.rows):
            for col in range(dim.cols):
                s += "|"
                if (row, col) in self:
                    s += str(self[row, col])
                else:
                    s += " "
            s += "|\n"
            for col in range(dim.cols):
                s += "+-"
            s += "+\n"
        return s

    def __len__(self) -> int:
        return len(self._pieces)

    def __iter__(self) -> Iterator[_Piece]:
        return iter(self._pieces)

    def __getitem__(self, key: pos.Pos | tuple[int, int]) -> _Piece:
        match key:
            case pos.Pos():
                return self.pieces_by_pos[key]
            case row, col:
                return self.pieces_by_pos[pos.Pos(row, col)]
            case _:
                raise TypeError(key)

    def __contains__(self, key: object) -> bool:
        match key:
            case piece.Piece():
                return key in self._pieces
            case pos.Pos():
                return key in self.pieces_by_pos
            case (row, col):
                if isinstance(row, int) and isinstance(col, int):
                    return pos.Pos(row, col) in self.pieces_by_pos
        raise TypeError(key)

    def with_piece(self, piece: _Piece) -> Self:
        return self.__class__(self._pieces | {piece})


from gbge.player import player
from gbge.board.grid import piece
