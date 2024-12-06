import time
import numpy as np
from state.Action import get_action_from_rerolls, AssignAction, get_action_from_index, RerollAction
from state.Category import Category
from player.Player import Player
from state.State import transition
from utils.dice import check_yahtzee
from ai.Agent import QTableSerializer


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
        valid_actions = [action for action in self.state.get_valid_actions() if isinstance(action, RerollAction)]

        if not valid_actions:
            return None

        q_values = [self.q_table[self.state][action.index] for action in valid_actions]
        best_action_index = np.argmax(q_values)
        best_action = get_action_from_index(valid_actions[best_action_index].index)

        if isinstance(best_action, RerollAction):
            return best_action.rerolls
        return None

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
        valid_actions = [action for action in self.state.get_valid_actions() if isinstance(action, AssignAction)]

        if not valid_actions:
            print("No valid categories left to assign.")
            return

        q_values = [self.q_table[self.state][action.index] for action in valid_actions]
        best_action_index = np.argmax(q_values)
        best_action = valid_actions[best_action_index]
        best_category = next(category for category in self.state.scores.keys() if category.index == best_action.index)
        old_dice = self.state.dice
        self.state = transition(self.state, best_action)
        time.sleep(2)
        self._display_choice(old_dice, best_category)

