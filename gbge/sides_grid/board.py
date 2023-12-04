from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, MutableSet, Self, TypeVar
from gbge.grid import board


_Game = TypeVar("_Game", bound="game.Game")
_Player = TypeVar("_Player", bound="player.Player")
_Piece = TypeVar("_Piece", bound="piece.Piece")
_Result = TypeVar("_Result", bound="result.Result")
_Side = TypeVar("_Side", bound=Enum)


@dataclass(frozen=True)
class Board(
    Generic[
        _Game,
        _Player,
        _Piece,
        _Result,
        _Side,
    ],
    board.Board[
        _Game,
        _Player,
        _Piece,
        _Result,
    ],
):
    @classmethod
    @abstractmethod
    def piece(cls, player: _Player, pos: "pos.Pos") -> _Piece:
        ...

    @classmethod
    def load(cls, game: _Game, input: str) -> Self:
        dim = cls.dim()
        lines = input.split("\n")
        if len(lines) != dim.rows:
            raise ValueError(f"invalid lines len {len(lines)} expected {dim.rows}")
        pieces: MutableSet[_Piece] = set()
        for row, line in enumerate(lines):
            if len(line) != dim.cols:
                raise ValueError(
                    f"invalid line {repr(line)} len {len(line)} expected {dim.cols}"
                )
            for col, val in enumerate(line):
                if val != " ":
                    try:
                        side: _Side = game._side_type(val)
                    except Exception as error:
                        raise ValueError(f"invalid val {val} at {row} {col}: {error}")
                    pieces.add(cls.piece(game[side], pos.Pos(row, col)))
        return cls(game, frozenset(pieces))


from gbge.sides import game, player, result
from gbge.grid import piece, pos
