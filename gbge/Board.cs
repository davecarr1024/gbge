namespace gbge;

public abstract record IBoard<TGame, TState, TBoard, TPlayer>
    where TGame : IGame<TGame, TState, TBoard, TPlayer>
    where TState : IState<TGame, TState, TBoard, TPlayer>
    where TBoard : IBoard<TGame, TState, TBoard, TPlayer>
    where TPlayer : IPlayer<TGame, TState, TBoard, TPlayer>
{
    public abstract record Grid : IBoard<TGame, TState, TBoard, TPlayer>
    {
        public sealed record Pos
        {
            public Pos(uint row, uint col)
            {
                Row = row;
                Col = col;
            }

            public uint Row { get; init; }

            public uint Col { get; init; }
        }

        public abstract record Piece
        {
            public Piece(Pos pos) => Pos = pos;

            public Pos Pos { get; init; }
        }

        protected Grid(uint rows, uint cols, IImmutableDictionary<Pos, Piece> pieces)
        {
            Rows = rows;
            Cols = cols;
            Pieces = pieces;
            ValidatePieces();
        }

        private void ValidatePieces()
        {
            foreach (var item in Pieces)
            {
                if (item.Value.Pos != item.Key || item.Key.Row >= Rows || item.Key.Col >= Cols)
                {
                    throw new Exception($"invalid piece {item}");
                }
            }
        }

        public uint Rows { get; init; }

        public uint Cols { get; init; }

        public IImmutableDictionary<Pos, Piece> Pieces { get; init; }
    }
}