from unittest import TestCase
from gbge import grid


class PosTest(TestCase):
    def test_init_fail(self) -> None:
        for row, col, expected in list[tuple[int, int, bool]](
            [
                (-1, 0, False),
                (0, -1, False),
                (-1, -1, False),
                (0, 0, True),
            ]
        ):
            with self.subTest(row=row, col=col, expected=expected):
                if not expected:
                    with self.assertRaises(Exception):
                        grid.Pos(row, col)
                else:
                    grid.Pos(row, col)
