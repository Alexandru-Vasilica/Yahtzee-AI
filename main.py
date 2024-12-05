from game.YahtzeeGame import YahtzeeGame
from state.Category import categories


def main():
    game = YahtzeeGame(categories)
    game.play()


if __name__ == '__main__':
    main()