from dataclasses import dataclass, field
from typing import Mapping, Type
from gbge import sides
from toe import side


@dataclass(frozen=True)
class Game(
    sides.Game[
        "state.State",
        "player.Player",
        "result.Result",
        side.Side,
    ],
):
    _side_type: Type[side.Side] = field(
        init=False,
        default=side.Side,
    )

    @property
    def x(self) -> "player.Player":
        return self[side.Side.x]

    @property
    def o(self) -> "player.Player":
        return self[side.Side.o]

    @property
    def initial_state(self) -> "state.State":
        return state.State(
            self,
            board.Board(),
            self.x,
        )

    @staticmethod
    def main():
        print(
            Game(
                [
                    text_player.TextPlayer(side.Side.x),
                    text_player.TextPlayer(side.Side.o),
                ]
            ).run()
        )


from toe import board, player, state, result, text_player


if __name__ == "__main__":
    Game.main()
