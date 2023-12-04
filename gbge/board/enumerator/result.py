from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized, TypeVar


_Board = TypeVar("_Board", bound="board.Board")


@dataclass(frozen=True)
class Result(Generic[_Board], Sized, Iterable["Result[_Board]"]):
    board: _Board
    children: Sequence["Result[_Board]"] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator["Result[_Board]"]:
        return iter(self.children)


from gbge.board import board
