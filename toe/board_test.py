from dataclasses import dataclass
from typing import Optional
from unittest import TestCase
import toe


@dataclass(frozen=True)
class _Player(toe.Player):
    def move(self, board: toe.Board) -> toe.Board:
        raise NotImplementedError()


class BoardTest(TestCase):
    def test_result(self) -> None:
        game = toe.Game([_Player(toe.Side.x), _Player(toe.Side.o)])
        for board, expected in list[
            tuple[
                toe.Board,
                Optional[toe.Result],
            ]
        ](
            [
                (
                    toe.Board(game),
                    None,
                ),
                (
                    toe.Board.load(game, "xxx\n   \n   "),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "   \nxxx\n   "),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "   \n   \nxxx"),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "x  \nx  \nx  "),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, " x \n x \n x "),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "  x\n  x\n  x"),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "x  \n x \n  x"),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "  x\n x \nx  "),
                    toe.Result(toe.Side.x),
                ),
                (
                    toe.Board.load(game, "ooo\n   \n   "),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "   \nooo\n   "),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "   \n   \nooo"),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "o  \no  \no  "),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, " o \n o \n o "),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "  o\n  o\n  o"),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "o  \n o \n  o"),
                    toe.Result(toe.Side.o),
                ),
                (
                    toe.Board.load(game, "  o\n o \no  "),
                    toe.Result(toe.Side.o),
                ),
            ]
        ):
            with self.subTest(
                board=str(board),
                expected=str(expected),
            ):
                self.assertEqual(board.result(), expected)
