namespace gbge;

public abstract record IState<TGame, TState, TBoard, TPlayer>
    where TGame : IGame<TGame, TState, TBoard, TPlayer>
    where TState : IState<TGame, TState, TBoard, TPlayer>
    where TBoard : IBoard<TGame, TState, TBoard, TPlayer>
    where TPlayer : IPlayer<TGame, TState, TBoard, TPlayer>
{
    public IState(TGame game, TBoard board, TPlayer player)
    {
        Game = game;
        Board = board;
        Player = player;
    }

    public TGame Game { get; init; }

    public TBoard Board { get; init; }

    public TPlayer Player { get; init; }

    public abstract ISet<TState> Moves();
}