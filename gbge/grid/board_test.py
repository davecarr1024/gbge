from dataclasses import dataclass
from typing import FrozenSet, Optional
from unittest import TestCase
import gbge


@dataclass(frozen=True)
class _Game(
    gbge.Game[
        "_Board",
        "_Player",
        "_Result",
    ]
):
    def initial_board(self) -> "_Board":
        return _Board(self)


@dataclass(frozen=True)
class _Board(
    gbge.grid.Board[
        "_Game",
        "_Player",
        "_Piece",
        "_Result",
    ],
):
    @classmethod
    def dim(cls) -> gbge.grid.Dim:
        return gbge.grid.Dim(2, 2)

    def moves(self, player: "_Player") -> FrozenSet["_Board"]:
        return frozenset()

    def result(self) -> Optional["_Result"]:
        return None


@dataclass(frozen=True)
class _Piece(
    gbge.grid.Piece["_Player"],
):
    ...


@dataclass(frozen=True)
class _Player(gbge.Player["_Board"]):
    name: str

    def __str__(self) -> str:
        return self.name

    def move(self, board: "_Board") -> "_Board":
        raise NotImplementedError()


@dataclass(frozen=True)
class _Result:
    ...


_game = _Game([])


class BoardTest(TestCase):
    def test_invalid_piece(self) -> None:
        with self.assertRaises(Exception):
            _Board(_game, frozenset([_Piece(_Player("a"), gbge.grid.Pos(2, 2))]))

    def test_contains(self) -> None:
        for lhs, board, expected in list[
            tuple[
                _Piece | gbge.grid.Pos | tuple[int, int],
                _Board,
                bool,
            ]
        ](
            [
                (
                    _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                    _Board(
                        _game,
                    ),
                    False,
                ),
                (
                    gbge.grid.Pos(0, 0),
                    _Board(
                        _game,
                    ),
                    False,
                ),
                (
                    (0, 0),
                    _Board(
                        _game,
                    ),
                    False,
                ),
                (
                    _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    True,
                ),
                (
                    gbge.grid.Pos(0, 0),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    True,
                ),
                (
                    (0, 0),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    True,
                ),
            ]
        ):
            with self.subTest(lhs=lhs, board=board, expected=expected):
                if expected:
                    self.assertIn(lhs, board)
                else:
                    self.assertNotIn(lhs, board)

    def test_getitem(self) -> None:
        for lhs, board, expected in list[
            tuple[
                gbge.grid.Pos | tuple[int, int],
                _Board,
                Optional[_Piece],
            ]
        ](
            [
                (
                    gbge.grid.Pos(0, 0),
                    _Board(
                        _game,
                    ),
                    None,
                ),
                (
                    (0, 0),
                    _Board(
                        _game,
                    ),
                    None,
                ),
                (
                    gbge.grid.Pos(0, 0),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                ),
                (
                    (0, 0),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, board=board, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        board[lhs]
                else:
                    self.assertEqual(board[lhs], expected)

    def test_or(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                _Board,
                _Piece | _Board,
                Optional[_Board],
            ]
        ](
            [
                (
                    _Board(
                        _game,
                    ),
                    _Board(
                        _game,
                    ),
                    _Board(
                        _game,
                    ),
                ),
                (
                    _Board(
                        _game,
                    ),
                    _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                ),
                (
                    _Board(
                        _game,
                    ),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                ),
                (
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(_Player("b"), gbge.grid.Pos(0, 0)),
                    None,
                ),
                (
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("b"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    None,
                ),
                (
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(_Player("b"), gbge.grid.Pos(1, 0)),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                                _Piece(_Player("b"), gbge.grid.Pos(1, 0)),
                            ]
                        ),
                    ),
                ),
                (
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("b"), gbge.grid.Pos(1, 0)),
                            ]
                        ),
                    ),
                    _Board(
                        _game,
                        frozenset(
                            [
                                _Piece(_Player("a"), gbge.grid.Pos(0, 0)),
                                _Piece(_Player("b"), gbge.grid.Pos(1, 0)),
                            ]
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        lhs | rhs
                else:
                    self.assertEqual(lhs | rhs, expected)
