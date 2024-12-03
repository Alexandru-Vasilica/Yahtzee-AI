from typing import TypedDict


class Category:
    name: str
    description: str
    index: int

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        pass

    def __hash__(self):
        return hash(self.index)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class DiceValueCategory(Category):
    value: int

    def __init__(self, name: str, description: str, value: int):
        self.index = value - 1
        self.name = name
        self.description = description
        self.value = value

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        if joker_rule:
            return 5 * self.value
        return self.value * dice.count(self.value)


class Chance(Category):

    def __init__(self):
        self.index = 11
        self.name = 'Chance'
        self.description = 'Sum of all dice'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        return sum(dice)


class Ones(DiceValueCategory):
    def __init__(self):
        super().__init__('Ones', 'Sum of all ones', 1)


class Twos(DiceValueCategory):
    def __init__(self):
        super().__init__('Twos', 'Sum of all twos', 2)


class Threes(DiceValueCategory):
    def __init__(self):
        super().__init__('Threes', 'Sum of all threes', 3)


class Fours(DiceValueCategory):
    def __init__(self):
        super().__init__('Fours', 'Sum of all fours', 4)


class Fives(DiceValueCategory):
    def __init__(self):
        super().__init__('Fives', 'Sum of all fives', 5)


class Sixes(DiceValueCategory):
    def __init__(self):
        super().__init__('Sixes', 'Sum of all sixes', 6)


class ThreeOfAKind(Category):

    def __init__(self):
        self.index = 6
        self.name = 'Three of a Kind'
        self.description = 'Sum of all dice if 3 are the same'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        for i in range(1, 7):
            if dice.count(i) >= 3:
                return sum(dice)
        return 0


class FourOfAKind(Category):

    def __init__(self):
        self.index = 7
        self.name = 'Four of a Kind'
        self.description = 'Sum of all dice if 4 are the same'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        for i in range(1, 7):
            if dice.count(i) >= 4:
                return sum(dice)
        return 0


class FullHouse(Category):

    def __init__(self):
        self.index = 8
        self.name = 'Full House'
        self.description = '25 if 3 of a kind and 2 of a kind'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        if joker_rule:
            return 25
        threeDices = False
        twoDices = False
        for i in range(1, 7):
            if dice.count(i) == 3:
                threeDices = True
            if dice.count(i) == 2:
                twoDices = True
        if threeDices and twoDices:
            return 25
        return 0


class SmallStraight(Category):

    def __init__(self):
        self.index = 9
        self.name = 'Small Straight'
        self.description = '30 if 4 in a row'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        if joker_rule:
            return 30
        sortedDice = sorted(set(dice))
        SmallStraights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        for i in SmallStraights:
            if i.issubset(sortedDice):
                return 30
        return 0


class LargeStraight(Category):

    def __init__(self):
        self.index = 10
        self.name = 'Large Straight'
        self.description = '40 if 5 in a row'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        if joker_rule:
            return 40
        sortedDice = sorted(set(dice))
        LargeStraights = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
        for i in LargeStraights:
            if i.issubset(sortedDice):
                return 40
        return 0


class Yahtzee(Category):

    def __init__(self):
        self.index = 12
        self.name = 'Yahtzee'
        self.description = '50 if all dice are the same'

    def get_score(self, dice: list[int], joker_rule=False) -> int:
        if len(set(dice)) == 1:
            return 50
        return 0


categories = [Ones(), Twos(), Threes(), Fours(), Fives(), Sixes(),
              Chance(), SmallStraight(), LargeStraight(), FullHouse(), ThreeOfAKind(),
              FourOfAKind(), Yahtzee()]
