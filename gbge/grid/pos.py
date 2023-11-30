from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def __post_init__(self) -> None:
        assert self.row >= 0 and self.col >= 0
