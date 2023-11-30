from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Sequence, Type
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
        raise NotImplementedError()


@dataclass(frozen=True)
class _Board(gbge.Board["_Game", "_Player", "_Result"]):
    ...


@dataclass(frozen=True)
class _Player(gbge.sides.Player["_Board", "_Side"]):
    def move(self, board: "_Board") -> "_Board":
        raise NotImplementedError()


@dataclass(frozen=True)
class _Result(gbge.sides.Result["_Side"]):
    ...


class GameTest(TestCase):
    def test_invalid_players(self):
        for players, expected in list[
            tuple[
                Sequence[_Player],
                bool,
            ]
        ](
            [
                (
                    [],
                    False,
                ),
                (
                    [
                        _Player(_Side.a),
                    ],
                    False,
                ),
                (
                    [
                        _Player(_Side.b),
                    ],
                    False,
                ),
                (
                    [
                        _Player(_Side.b),
                        _Player(_Side.b),
                    ],
                    False,
                ),
                (
                    [
                        _Player(_Side.a),
                        _Player(_Side.b),
                        _Player(_Side.b),
                    ],
                    False,
                ),
                (
                    [
                        _Player(_Side.a),
                        _Player(_Side.b),
                    ],
                    True,
                ),
            ]
        ):
            with self.subTest(players=players, expected=expected):
                if not expected:
                    with self.assertRaises(Exception):
                        _Game(players)
                else:
                    _Game(players)
