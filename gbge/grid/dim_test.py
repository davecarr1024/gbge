from unittest import TestCase

from gbge import grid


class DimTest(TestCase):
    def test_contains(self) -> None:
        for pos, dim, expected in list[
            tuple[
                grid.Pos,
                grid.Dim,
                bool,
            ]
        ](
            [
                (
                    grid.Pos(0, 0),
                    grid.Dim(1, 1),
                    True,
                ),
                (
                    grid.Pos(0, 1),
                    grid.Dim(1, 1),
                    False,
                ),
                (
                    grid.Pos(1, 0),
                    grid.Dim(1, 1),
                    False,
                ),
                (
                    grid.Pos(1, 1),
                    grid.Dim(1, 1),
                    False,
                ),
            ]
        ):
            with self.subTest(pos=pos, dim=dim, expected=expected):
                if expected:
                    self.assertIn(pos, dim)
                else:
                    self.assertNotIn(pos, dim)
