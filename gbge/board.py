from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import (
    FrozenSet,
    Iterable,
    Iterator,
    Mapping,
    MutableSet,
    Optional,
    Self,
    Sequence,
    Sized,
    Union,
)


class Board(ABC):
    @dataclass(frozen=True)
    class Tree(Sized, Iterable["Board.Tree"]):
        class Factory(ABC):
            @abstractmethod
            def __call__(
                self,
                board: "Board",
                player: "player.Player",
            ) -> "Board.Tree":
                ...

        @dataclass(frozen=True)
        class Full(Factory):
            game: "game.Game"

            def __call__(
                self,
                board: "Board",
                player: "player.Player",
            ) -> "Board.Tree":
                return Board.Tree(
                    board,
                    frozenset(
                        [
                            self(child, self.game.next_player(player))
                            for child in board.moves(self.game, player)
                        ]
                    ),
                )

        @dataclass(frozen=True)
        class MaxDepth(Factory):
            game: "game.Game"
            max_depth: int

            def __call__(
                self, board: "Board", player_: "player.Player"
            ) -> "Board.Tree":
                def iter(
                    board: "Board", player_: "player.Player", depth: int
                ) -> "Board.Tree":
                    if depth >= self.max_depth:
                        return Board.Tree(board)
                    return Board.Tree(
                        board,
                        frozenset(
                            [
                                iter(child, self.game.next_player(player_), depth + 1)
                                for child in board.moves(self.game, player_)
                            ]
                        ),
                    )

                return iter(board, player_, 1)

        board: "Board"
        children: FrozenSet["Board.Tree"] = field(default_factory=frozenset)

        def __len__(self) -> int:
            return len(self.children)

        def __iter__(self) -> Iterator["Board.Tree"]:
            return iter(self.children)

    class Search(ABC):
        @dataclass(frozen=True)
        class Result:
            board: "Board"
            value: float
            child: Optional["Board.Search.Result"] = None

            def with_parent(
                self, board: "Board", value: float
            ) -> "Board.Search.Result":
                return Board.Search.Result(board, value, self)

        @abstractmethod
        def __call__(
            self, board: "Board", player: "player.Player"
        ) -> "Board.Search.Result":
            ...

    @dataclass(frozen=True)
    class MinMax(Search):
        game: "game.Game"
        tree_factory: "Board.Tree.Factory"
        evaluator: "Board.Evaluator"

        def __call__(
            self, board: "Board", player_: "player.Player"
        ) -> "Board.Search.Result":
            def iter(
                tree: "Board.Tree", tree_player: "player.Player"
            ) -> "Board.Search.Result":
                value = self.evaluator(tree.board, tree_player)
                if len(tree) == 0:
                    return Board.Search.Result(tree.board, value)
                next_player = self.game.next_player(tree_player)
                child_results = [iter(child, next_player) for child in tree]
                return (max if tree_player == player_ else min)(
                    child_results, key=lambda result: result.value
                ).with_parent(tree.board, value)

            return iter(self.tree_factory(board, player_), player_)

    class Evaluator(ABC):
        @abstractmethod
        def __call__(self, board: "Board", player: "player.Player") -> float:
            ...

    @abstractmethod
    def moves(self, game: "game.Game", player: "player.Player") -> FrozenSet["Board"]:
        ...

    @abstractmethod
    def result(self) -> Optional["game.Game.Result"]:
        ...


@dataclass(frozen=True)
class Grid(Board, Mapping["Grid.Pos", "Grid.Piece"]):
    @dataclass(frozen=True)
    class Dim:
        rows: int
        cols: int

        def __contains__(self, rhs: object) -> bool:
            match rhs:
                case Grid.Pos():
                    return 0 <= rhs.row < self.rows and 0 <= rhs.col < self.cols
                case Grid.Piece():
                    return rhs.pos in self
                case _:
                    raise TypeError(rhs)

    @dataclass(frozen=True)
    class Pos:
        row: int
        col: int

    @dataclass(frozen=True)
    class Piece:
        pos: "Grid.Pos"
        player: "player.Player"

        def __str__(self) -> str:
            return str(self.player)

    pieces: FrozenSet["Grid.Piece"] = field(default_factory=frozenset)

    @classmethod
    @abstractmethod
    def dim(cls) -> "Grid.Dim":
        ...

    @cached_property
    def pieces_by_pos(self) -> Mapping["Grid.Pos", "Grid.Piece"]:
        return {piece.pos: piece for piece in self.pieces}

    def __post_init__(self) -> None:
        assert len(self.pieces) == len(self.pieces_by_pos), "duplicate piece pos"

    def __len__(self) -> int:
        return len(self.pieces_by_pos)

    def __iter__(self) -> Iterator["Grid.Pos"]:
        return iter(self.pieces_by_pos)

    def __getitem__(self, key: "Grid.Pos") -> "Grid.Piece":
        return self.pieces_by_pos[key]

    def __str__(self) -> str:
        def piece_str(row: int, col: int) -> str:
            pos = Grid.Pos(row, col)
            if pos in self:
                return str(self[pos])
            else:
                return " "

        dim = self.dim()
        return "\n".join(
            "".join(piece_str(row, col) for col in range(dim.cols))
            for row in range(dim.rows)
        )

    def __or__(self, rhs: Union["Grid", "Grid.Piece"]) -> Self:
        match rhs:
            case Grid():
                return self.__class__(self.pieces | rhs.pieces)
            case Grid.Piece():
                return self.__class__(self.pieces | {rhs})
            case _:
                raise TypeError(rhs)


@dataclass(frozen=True)
class MoveEmptyGrid(Grid):
    def moves(self, game: "game.Game", player: "player.Player") -> FrozenSet["Board"]:
        dim = self.dim()
        moves: MutableSet["Board"]
        for row in range(dim.rows):
            for col in range(dim.cols):
                pos = Grid.Pos(row, col)
                if pos not in self:
                    moves.add(self | self.Piece(pos, player))
        return frozenset(moves)


from gbge import game, player
