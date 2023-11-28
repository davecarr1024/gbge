namespace gbge;

public abstract record IPlayer<TGame, TState, TBoard, TPlayer>
    where TGame : IGame<TGame, TState, TBoard, TPlayer>
    where TState : IState<TGame, TState, TBoard, TPlayer>
    where TBoard : IBoard<TGame, TState, TBoard, TPlayer>
    where TPlayer : IPlayer<TGame, TState, TBoard, TPlayer>
{
    public abstract TState Move(TState state);
}