import time

import numpy

from game.Category import Category
from player.Player import Player


class AiPlayer(Player):

    def __init__(self,name:str,categories:list[Category]):
        super().__init__(name,categories)

    def play_turn(self):
        self._display_player_turn()
        self.roll_dice(list(range(5)))
        self.handle_rerolls()
        is_yahtzee = self.verify_yahtzee()
        joker_rule = False
        if is_yahtzee:
            joker_rule = self.handle_yahtzee()
        self.chose_category(joker_rule)
        self.reset_dice()

    def get_rerolls(self):
        if numpy.random.rand() > 0.5:
            return None
        should_reroll_die = numpy.random.rand(5) > 0.5
        return [i for i, x in enumerate(should_reroll_die) if x]

    def handle_rerolls(self):
        for _ in range(2):
            rerolls = self.get_rerolls()
            if rerolls is None:
                return
            time.sleep(2)
            print(f'Rerolling dice: {rerolls}')
            self.roll_dice(rerolls)

    def chose_category(self, joker_rule=False):
        valid_categories = [category for category, score in self.scorecard.items() if score is None]
        best_category = max(valid_categories, key=lambda category: category.get_score(self.dice, joker_rule))
        self.check_scorecard(best_category, joker_rule)
        time.sleep(2)
        self._display_choice(best_category)