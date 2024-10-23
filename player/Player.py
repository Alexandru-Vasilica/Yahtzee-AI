from numpy.random import randint

from game import Category


class Player:
    name: str
    dice: list[int | None]
    scorecard: dict[Category, int | None]

    def __init__(self, name: str, categories: list[Category]):
        self.name = name
        self.score = 0
        self.dice = [None, None, None, None, None]
        self.scorecard = {}
        for category in categories:
            self.scorecard[category] = None

    def roll_dice(self, dice_indexes: list[int]):
        for index in dice_indexes:
            if index < 0 or index > 4:
                print('Invalid dice index')
                continue
            self.dice[index] = randint(1, 6)
        self._display_dice()

    def _display_dice(self):
        print(f'{self.name} rolls: ')
        for idx, dice in enumerate(self.dice):
            print(f'Dice {idx + 1}: {dice}')

    def check_scorecard(self, category: Category):
        self.scorecard[category] = category.get_score(self.dice)

    def _display_choice(self, category: Category):
        print(f'{self.name} chose {category.name} with a {self.dice} roll and scored {self.scorecard[category]} points')

    def _display_player_turn(self):
        print(f'----{self.name}\'s ----')

    def reset_dice(self):
        self.dice = [None, None, None, None, None]

    def get_score(self):
        return sum([score for score in self.scorecard.values() if score is not None])

    def handle_rerolls(self):
        pass

    def chose_category(self):
        pass

    def play_turn(self):
        pass
