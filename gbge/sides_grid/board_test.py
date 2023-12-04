from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import FrozenSet, Optional, Type
from unittest import TestCase
import gbge


class _Side(StrEnum):
    a = auto()
    b = auto()


@dataclass(frozen=True)
class _Game(
    gbge.sides.Game[
        "_Board",
        "_Player",
        "_Result",
        "_Side",
    ]
):
    _side_type: Type["_Side"] = field(default=_Side, init=False)

    def initial_board(self) -> "_Board":
        return _Board(self)


@dataclass(frozen=True)
class _Board(
    gbge.sides_grid.Board[
        "_Game",
        "_Player",
        "_Piece",
        "_Result",
        "_Side",
    ]
):
    @classmethod
    def dim(self) -> gbge.grid.Dim:
        return gbge.grid.Dim(2, 2)

    @classmethod
    def piece(cls, player: "_Player", pos: gbge.grid.Pos) -> "_Piece":
        return _Piece(player, pos)

    def moves(self, player: "_Player") -> FrozenSet["_Board"]:
        return frozenset()

    def result(self) -> Optional["_Result"]:
        return None


@dataclass(frozen=True)
class _Piece(gbge.grid.Piece["_Player"]):
    ...


@dataclass(frozen=True)
class _Player(
    gbge.sides.Player[
        "_Board",
        "_Side",
    ]
):
    def move(self, board: _Board) -> _Board:
        raise NotImplementedError()


@dataclass(frozen=True)
class _Result(gbge.sides.Result["_Side"]):
    ...


class BoardTest(TestCase):
    def test_load(self) -> None:
        game = _Game([_Player(_Side.a), _Player(_Side.b)])
        for input, expected in list[
            tuple[
                str,
                Optional[_Board],
            ]
        ](
            [
                (
                    "",
                    None,
                ),
                (
                    "aa\nbb\naa",
                    None,
                ),
                (
                    "aa\nbbb",
                    None,
                ),
                (
                    "aa\nbc",
                    None,
                ),
                (
                    "  \n  ",
                    _Board(game),
                ),
                (
                    "a \n  ",
                    _Board(
                        game,
                        frozenset(
                            [
                                _Piece(
                                    _Player(_Side.a),
                                    gbge.grid.Pos(0, 0),
                                ),
                            ]
                        ),
                    ),
                ),
                (
                    "a \n b",
                    _Board(
                        game,
                        frozenset(
                            [
                                _Piece(
                                    _Player(_Side.a),
                                    gbge.grid.Pos(0, 0),
                                ),
                                _Piece(
                                    _Player(_Side.b),
                                    gbge.grid.Pos(1, 1),
                                ),
                            ]
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        _Board.load(game, input)
                else:
                    self.assertEqual(_Board.load(game, input), expected)
