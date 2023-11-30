from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, Sequence, Sized, TypeVar

_State = TypeVar("_State", bound="state.State")
_Player = TypeVar("_Player", bound="player.Player")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Game(
    ABC,
    Generic[_State, _Player, _Result],
):
    players: Sequence[_Player]

    @property
    @abstractmethod
    def initial_state(self) -> _State:
        ...

    def next_player(self, player: _Player) -> _Player:
        return self.players[(self.players.index(player) + 1) % len(self.players)]

    def run(self) -> _Result:
        state = self.initial_state
        while state.result is None:
            state = state.move()
        return state.result


from gbge.state import state
from gbge.player import player
