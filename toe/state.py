from dataclasses import dataclass

from gbge import state


@dataclass(frozen=True)
class State(
    state.State[
        "game.Game",
        "board.Board",
        "player.Player",
        "result.Result",
    ],
):
    ...


from toe import game, board, player, result
