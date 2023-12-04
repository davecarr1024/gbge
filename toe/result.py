from dataclasses import dataclass
import gbge


@dataclass(frozen=True)
class Result(gbge.sides.Result["side.Side"]):
    ...


from toe import side
