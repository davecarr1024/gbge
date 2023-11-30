from typing import Optional
from unittest import TestCase
from gbge.board import grid
import toe


class _Player(toe.Player):
    def move(self, state: toe.State) -> toe.Board:
        raise NotImplementedError()


_game = toe.Game(
    {
        toe.Side.x: _Player(toe.Side.x),
        toe.Side.o: _Player(toe.Side.o),
    }
)


class BoardTest(TestCase):
    def test_load(self) -> None:
        for input, expected in list[
            tuple[
                str,
                Optional[toe.Board],
            ]
        ](
            [
                (
                    "",
                    None,
                ),
                (
                    "   \n   \n   ",
                    toe.Board(),
                ),
                (
                    "   \n   \n x ",
                    toe.Board(
                        frozenset(
                            [
                                toe.Piece(
                                    _game.x,
                                    grid.Pos(2, 1),
                                ),
                            ]
                        )
                    ),
                ),
                (
                    "  o\n   \n x ",
                    toe.Board(
                        frozenset(
                            [
                                toe.Piece(
                                    _game.x,
                                    grid.Pos(2, 1),
                                ),
                                toe.Piece(
                                    _game.o,
                                    grid.Pos(0, 2),
                                ),
                            ]
                        )
                    ),
                ),
                (
                    "   \n   \n  a",
                    None,
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(Exception):
                        toe.Board.load(_game, input)
                else:
                    self.assertEqual(toe.Board.load(_game, input), expected)

    def test_moves(self) -> None:
        for board, player, expected in list[
            tuple[
                toe.Board,
                toe.Player,
                frozenset[toe.Board],
            ]
        ](
            [
                (
                    toe.Board.load(_game, "xxx\nxxx\nxxx"),
                    _game.o,
                    frozenset(),
                ),
                (
                    toe.Board.load(_game, "xxx\nxxx\nxx "),
                    _game.o,
                    frozenset(
                        [
                            toe.Board.load(_game, "xxx\nxxx\nxxo"),
                        ]
                    ),
                ),
                (
                    toe.Board.load(_game, "xxx\nxxx\n   "),
                    _game.o,
                    frozenset(
                        [
                            toe.Board.load(_game, "xxx\nxxx\no  "),
                            toe.Board.load(_game, "xxx\nxxx\n o "),
                            toe.Board.load(_game, "xxx\nxxx\n  o"),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(board=board, player=player, expected=expected):
                self.assertSetEqual(
                    frozenset(board.moves(player)),
                    frozenset(expected),
                )
