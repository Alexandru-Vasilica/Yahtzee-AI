import time

import numpy

from state.Action import get_action_from_rerolls, AssignAction, get_action_from_index, RerollAction
from state.Category import Category
from player.Player import Player
from state.State import transition
from utils.dice import check_yahtzee
from ai.Environment import QTableSerializer


class AiPlayer(Player):

    def __init__(self, name: str, categories: list[Category], q_table_path: str):
        super().__init__(name, categories)
        self.q_table = QTableSerializer.load(q_table_path)

    def play_turn(self):
        self._display_player_turn()
        self.handle_rerolls()
        joker_rule = False
        if check_yahtzee(self.state.dice):
            print('Yahtzee!')
            joker_rule = self.state.yahtzee_count > 0
        self.chose_category(joker_rule)

    def get_rerolls(self):
        valid_actions = [
            action for action in self.state.get_valid_actions()
            if isinstance(get_action_from_index(action.index), RerollAction)
        ]
        if not valid_actions:
            return None
        q_values = {action: self.q_table[self.state][action.index] for action in valid_actions}
        best_action = max(q_values, key=q_values.get)
        return best_action.rerolls

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
        valid_actions = [
            action for action in self.state.get_valid_actions()
            if isinstance(get_action_from_index(action.index), AssignAction)
        ]
        if not valid_actions:
            return
        q_values = {action: self.q_table[self.state][action.index] for action in valid_actions}
        best_action = max(q_values, key=q_values.get)
        category = next(category for category in self.state.scores.keys() if category.index == best_action.index)
        old_dice = self.state.dice
        action = AssignAction(category.index)
        self.state = transition(self.state, action)
        time.sleep(2)
        self._display_choice(old_dice, category)
