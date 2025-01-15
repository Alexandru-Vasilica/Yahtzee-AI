import time

import numpy

from player.Strategy import Strategy
from state.Action import get_action_from_rerolls, AssignAction, get_action_from_index, RerollAction, Action, \
    ASSIGN_ACTION_BOUNDARY
from state.Category import Category
from player.Player import Player
from state.State import transition
from utils.dice import check_yahtzee
from ai.Environment import QTableSerializer


class AiPlayer(Player):
    strategy: Strategy
    action: Action | None

    def __init__(self, name: str, categories: list[Category], strategy):
        super().__init__(name, categories)
        self.strategy = strategy
        self.action = None

    def play_turn(self):
        self._display_player_turn()
        self.action = self.strategy.choose_action(self.state)
        self.handle_rerolls()
        joker_rule = False
        if check_yahtzee(self.state.dice):
            print('Yahtzee!')
            joker_rule = self.state.yahtzee_count > 0
        self.chose_category(joker_rule)

    def get_rerolls(self):
        if self.action.index <= ASSIGN_ACTION_BOUNDARY:
            return None
        return self.action.rerolls

    def handle_rerolls(self):
        rerolls = self.get_rerolls()
        if rerolls is None:
            return
        print(f'Rerolling dice: {rerolls}')
        self.state = transition(self.state, self.action)
        self._display_dice()
        self.action = self.strategy.choose_action(self.state)

    def chose_category(self, joker_rule=False):
        category = next((category for category in self.state.scores.keys() if category.index == self.action.index), None)
        old_dice = self.state.dice
        self.state = transition(self.state, self.action)
        time.sleep(2)
        self._display_choice(old_dice, category)
