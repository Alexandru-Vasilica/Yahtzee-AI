import numpy

from game import Category
from game.Category import DiceValueCategory


class Player:
    name: str
    dice: list[int | None]
    scorecard: dict[Category, int | None]
    yahtzee_count: int

    def __init__(self, name: str, categories: list[Category]):
        self.name = name
        self.score = 0
        self.dice = [None, None, None, None, None]
        self.scorecard = {}
        self.yahtzee_count = 0
        self.joker_rule_applied = False
        for category in categories:
            self.scorecard[category] = None

    def roll_dice(self, dice_indexes: list[int]):
        for index in dice_indexes:
            if index < 0 or index > 4:
                print('Invalid dice index')
                continue
            #self.dice[index] = numpy.random.randint(1, 7)
            self.dice[index] = 5
        self._display_dice()

    def _display_dice(self):
        print(f'{self.name} rolls: ')
        for idx, dice in enumerate(self.dice):
            print(f'Dice {idx + 1}: {dice}')

    def verify_yahtzee(self):
        if len(set(self.dice)) == 1:
            return True
        return False

    def handle_yahtzee(self):
        for category in self.scorecard.keys():
            if category.name == 'Yahtzee' and self.scorecard[category] is not None:
                self.yahtzee_count += 1
                print(f'{self.name} scored a Yahtzee! {self.yahtzee_count} Yahtzees so far')
                return True
        return False

    def check_scorecard(self, category: Category, joker_rule=False):
        self.scorecard[category] = category.get_score(self.dice, joker_rule)

    def _display_choice(self, category: Category):
        print(f'{self.name} chose {category.name} with a {self.dice} roll and scored {self.scorecard[category]} points')

    def _display_player_turn(self):
        print(f'----{self.name}\'s ----')

    def reset_dice(self):
        self.dice = [None, None, None, None, None]

    def get_score(self):
        return (sum([score for score in self.scorecard.values() if score is not None]) +
                self.get_bonus() + self.yahtzee_count * 100)

    def get_bonus(self):
        bonus = 0
        score = 0
        for category in self.scorecard.keys():
            if isinstance(category, DiceValueCategory) and self.scorecard[category] is not None:
                score += self.scorecard[category]
        if score >= 63:
            bonus = 35
        return bonus

    def handle_rerolls(self):
        pass

    def chose_category(self, joker_rule=False):
        pass

    def play_turn(self):
        pass
