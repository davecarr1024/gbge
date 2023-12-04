from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional
import gbge


@dataclass(frozen=True)
class Result(gbge.sides.Result["side.Side"]):
    class Type(StrEnum):
        win = auto()
        tie = auto()

    type: Type = Type.win


from toe import side
