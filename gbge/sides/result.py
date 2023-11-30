from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


_Side = TypeVar("_Side", bound=Enum)


@dataclass(frozen=True)
class Result(Generic[_Side]):
    side: _Side
