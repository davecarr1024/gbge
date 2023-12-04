from toe import game, side, text_player


def main():
    print(
        game.Game(
            [
                text_player.TextPlayer(side.Side.x),
                text_player.TextPlayer(side.Side.o),
            ]
        ).run()
    )


if __name__ == "__main__":
    main()
