from unittest import TestCase
import toe


class BoardTest(TestCase):
    def test_init(self) -> None:
        self.assertEqual(toe.Board(), toe.Board())
