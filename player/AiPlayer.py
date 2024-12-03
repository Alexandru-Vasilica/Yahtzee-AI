import time

import numpy

from state.Action import get_action_from_rerolls, AssignAction
from state.Category import Category
from player.Player import Player
from state.State import transition
from utils.dice import check_yahtzee


class AiPlayer(Player):

    def __init__(self, name: str, categories: list[Category]):
        super().__init__(name, categories)

    def play_turn(self):
        self._display_player_turn()
        self.handle_rerolls()
        joker_rule = False
        if check_yahtzee(self.state.dice):
            print('Yahtzee!')
            joker_rule = self.state.yahtzee_count > 0
        self.chose_category(joker_rule)

    def get_rerolls(self):
        if numpy.random.rand() > 0.5:
            return None
        should_reroll_die = numpy.random.rand(5) > 0.5
        return [i for i, x in enumerate(should_reroll_die) if x]

    def handle_rerolls(self):
        while self.state.rerolls_left > 0:
            rerolls = self.get_rerolls()
            if rerolls is None:
                return
            time.sleep(2)
            print(f'Rerolling dice: {rerolls}')
            action = get_action_from_rerolls(rerolls)
            self.state = transition(self.state, action)
            self._display_dice()

    def chose_category(self, joker_rule=False):
        valid_categories = [category for category, score in self.state.scores.items() if score is None]
        best_category = max(valid_categories, key=lambda category: category.get_score(self.state.dice, joker_rule))
        action = AssignAction(best_category.index)
        old_dice = self.state.dice
        self.state = transition(self.state, action)
        time.sleep(2)
        self._display_choice(old_dice, best_category)
