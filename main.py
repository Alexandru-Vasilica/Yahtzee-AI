from game.YahtzeeGame import YahtzeeGame
from game.Category import Sum,Ones


def main():
    game = YahtzeeGame([Sum(),Ones()])
    game.play()

if __name__ == '__main__':
    main()