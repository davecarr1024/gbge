from enum import StrEnum, auto


class Side(StrEnum):
    x = auto()
    o = auto()

    def other(self) -> "Side":
        match self:
            case Side.x:
                return Side.o
            case Side.o:
                return Side.x
