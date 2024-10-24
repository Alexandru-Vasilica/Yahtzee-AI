from game.YahtzeeGame import YahtzeeGame
import game.Category as Category


def main():
    game = YahtzeeGame([Category.Ones(), Category.Twos(), Category.Threes(), Category.Fours(), Category.Fives(), Category.Sixes(),
                        Category.Chance(), Category.SmallStraight(), Category.LargeStraight(), Category.FullHouse(), Category.ThreeOfAKind(),
                        Category.FourOfAKind(), Category.Yahtzee()])
    game.play()


if __name__ == '__main__':
    main()