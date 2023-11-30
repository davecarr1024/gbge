from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar

_Side = TypeVar("_Side", bound=StrEnum)


@dataclass(frozen=True)
class Result(Generic[_Side]):
    side: _Side
