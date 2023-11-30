from dataclasses import dataclass
from typing import FrozenSet, Optional, Sequence
from unittest import TestCase
from gbge.board import grid
from gbge.board.grid import pos
from gbge.game import game
from gbge.player import player
from gbge.state import state


@dataclass(frozen=True)
class _Game(game.Game["_Player"]):
    ...


@dataclass(frozen=True)
class _State(state.State["_Game", "_Board", "_Player"]):
    ...


@dataclass(frozen=True)
class _Player(player.Player["_State", "_Board"]):
    name: str

    def __post_init__(self) -> None:
        assert len(self.name) == 1, f"invalid name {self.name}"

    def __str__(self) -> str:
        return self.name

    def move(self, state: "_State") -> "_Board":
        raise NotImplementedError()


@dataclass(frozen=True)
class _Board(grid.Grid["_Player", "_Piece"]):
    @classmethod
    def dim(cls) -> "_Board.Dim":
        return _Board.Dim(3, 3)

    def moves(self, player: "_Player") -> FrozenSet["_Board"]:
        raise NotImplementedError()


@dataclass(frozen=True)
class _Piece(grid.Piece["_Player"]):
    ...


class GridTest(TestCase):
    def test_eq(self) -> None:
        self.assertEqual(_Board(), _Board())

    def test_new(self) -> None:
        for pieces, expected in list[
            tuple[
                FrozenSet[_Piece],
                Optional[_Board],
            ]
        ](
            [
                (
                    frozenset([]),
                    _Board(),
                ),
                (
                    frozenset(
                        [
                            _Piece(_Player("a"), pos.Pos(0, 0)),
                        ]
                    ),
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        ),
                    ),
                ),
                (
                    frozenset(
                        [
                            _Piece(_Player("a"), pos.Pos(0, 0)),
                            _Piece(_Player("b"), pos.Pos(0, 0)),
                        ]
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(pieces=pieces, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        _Board(pieces)
                else:
                    self.assertEqual(_Board(pieces), expected)

    def test_invalid_piece(self) -> None:
        player = _Player("a")
        for piece in list[_Piece](
            [
                _Piece(
                    player,
                    pos.Pos(-1, 0),
                ),
                _Piece(
                    player,
                    pos.Pos(0, -1),
                ),
                _Piece(
                    player,
                    pos.Pos(3, 0),
                ),
                _Piece(
                    player,
                    pos.Pos(0, 3),
                ),
            ]
        ):
            with self.subTest(piece=piece):
                with self.assertRaises(Exception):
                    _Board(frozenset([piece]))

    def test_with_piece(self) -> None:
        a = _Player("a")
        b = _Player("b")
        for board, piece, expected in list[
            tuple[
                _Board,
                _Piece,
                Optional[_Board],
            ]
        ](
            [
                (
                    _Board(),
                    _Piece(a, pos.Pos(0, 0)),
                    _Board(
                        frozenset(
                            [
                                _Piece(a, pos.Pos(0, 0)),
                            ]
                        ),
                    ),
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(b, pos.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(a, pos.Pos(0, 0)),
                    None,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(a, pos.Pos(0, 0)),
                            ]
                        ),
                    ),
                    _Piece(b, pos.Pos(1, 0)),
                    _Board(
                        frozenset(
                            [
                                _Piece(a, pos.Pos(0, 0)),
                                _Piece(b, pos.Pos(1, 0)),
                            ]
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(board=board, piece=piece, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        board.with_piece(piece)
                else:
                    self.assertEqual(board.with_piece(piece), expected)

    def test_getitem(self) -> None:
        for board, key, expected in list[
            tuple[
                _Board,
                pos.Pos | tuple[int, int],
                Optional[_Piece],
            ]
        ](
            [
                (
                    _Board(),
                    pos.Pos(0, 0),
                    None,
                ),
                (
                    _Board(),
                    (0, 0),
                    None,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    pos.Pos(0, 0),
                    _Piece(_Player("a"), pos.Pos(0, 0)),
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    (0, 0),
                    _Piece(_Player("a"), pos.Pos(0, 0)),
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    pos.Pos(1, 0),
                    None,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    (1, 0),
                    None,
                ),
            ]
        ):
            with self.subTest(board=board, key=key, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        board[key]
                else:
                    self.assertEqual(board[key], expected)

    def test_contains(self) -> None:
        for board, key, expected in list[
            tuple[_Board, pos.Pos | tuple[int, int], bool]
        ](
            [
                (
                    _Board(),
                    pos.Pos(0, 0),
                    False,
                ),
                (
                    _Board(),
                    (0, 0),
                    False,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    pos.Pos(0, 0),
                    True,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    (0, 0),
                    True,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    pos.Pos(1, 0),
                    False,
                ),
                (
                    _Board(
                        frozenset(
                            [
                                _Piece(_Player("a"), pos.Pos(0, 0)),
                            ]
                        )
                    ),
                    (1, 0),
                    False,
                ),
            ]
        ):
            with self.subTest(board=board, key=key, expected=expected):
                if expected:
                    self.assertIn(key, board)
                else:
                    self.assertNotIn(key, board)
