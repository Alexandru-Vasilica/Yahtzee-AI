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
        self.chose_category()
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


    def chose_category(self):
        valid_categories = [category for category, score in self.scorecard.items() if score is None]
        best_category = max(valid_categories, key=lambda category: category.get_score(self.dice))
        self.check_scorecard(best_category)
        time.sleep(2)
        self._display_choice(best_category)
