from dataclasses import dataclass
from gbge.grid import pos


@dataclass(frozen=True)
class Dim:
    rows: int
    cols: int

    def __contains__(self, key: object) -> bool:
        match key:
            case pos.Pos():
                return key.row < self.rows and key.col < self.rows
            case _:
                raise TypeError(key)
