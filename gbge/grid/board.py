from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import FrozenSet, Generic, Iterator, Mapping, Self, TypeVar, cast
from gbge import board
from gbge.grid import dim, pos

_Game = TypeVar("_Game", bound="game.Game")
_Player = TypeVar("_Player", bound="player.Player")
_Piece = TypeVar("_Piece", bound="piece.Piece")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Board(
    Generic[
        _Game,
        _Player,
        _Piece,
        _Result,
    ],
    board.Board[_Game, _Player, _Result],
    Mapping[pos.Pos, _Piece],
):
    pieces: FrozenSet[_Piece] = field(default_factory=frozenset)

    @cached_property
    def pieces_by_pos(self) -> Mapping[pos.Pos, _Piece]:
        return {piece.pos: piece for piece in self.pieces}

    @classmethod
    @abstractmethod
    def dim(self) -> dim.Dim:
        ...

    def __post_init__(self) -> None:
        assert len(self.pieces_by_pos) == len(self.pieces), "duplicate piece pos"
        for piece in self.pieces:
            assert piece.pos in self.dim(), f"invalid piece {piece}"

    def __str__(self) -> str:
        s = ""
        dim = self.dim()
        s += f'{"+-"*dim.cols}+\n'
        for row in range(dim.rows):
            for col in range(dim.cols):
                s += f"|{str(self[row,col]) if (row,col) in self else ' '}"
            s += f"|\n{'+-'*dim.cols}+\n"
        return s

    def __len__(self) -> int:
        return len(self.pieces_by_pos)

    def __iter__(self) -> Iterator[pos.Pos]:
        return iter(self.pieces_by_pos)

    def __getitem__(self, key: pos.Pos | tuple[int, int]) -> _Piece:
        match key:
            case pos.Pos():
                return self.pieces_by_pos[key]
            case (row, col):
                return self.pieces_by_pos[pos.Pos(row, col)]
            case _:
                raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        match key:
            case piece.Piece():
                return key in self.pieces
            case pos.Pos():
                return key in self.pieces_by_pos
            case (row, col):
                if isinstance(row, int) and isinstance(col, int):
                    return pos.Pos(row, col) in self.pieces_by_pos
        raise TypeError(key)

    def __or__(self, rhs: _Piece | Self) -> Self:
        match rhs:
            case piece.Piece():
                return self.__class__(self.pieces | {cast(_Piece, rhs)})
            case Board():
                return self.__class__(self.pieces | rhs.pieces)
            case _:
                raise TypeError(rhs)

    def __sub__(self, rhs: _Piece | Self) -> Self:
        match rhs:
            case piece.Piece():
                return self.__class__(self.pieces - {cast(_Piece, rhs)})
            case Board():
                return self.__class__(self.pieces - rhs.pieces)
            case _:
                raise TypeError(rhs)

    def with_piece(self, piece: _Piece) -> Self:
        return self | piece

    def without_piece(self, piece: _Piece) -> Self:
        return self - piece

    def with_piece_at_pos(self, piece: _Piece, pos: pos.Pos) -> Self:
        return (self - piece) | piece.at_pos(pos)


from gbge import board, game, player
from gbge.grid import piece
