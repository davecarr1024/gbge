from dataclasses import dataclass
from gbge import sides
from toe import side


@dataclass(frozen=True)
class Result(sides.Result[side.Side]):
    ...
