from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    row: int
    col: int
