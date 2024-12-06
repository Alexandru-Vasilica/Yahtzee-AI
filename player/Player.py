from __future__ import annotations
import numpy
from state.State import State, get_starting_state
from state.Category import Category, DiceValueCategory


class Player:
    name: str
    state: State

    def __init__(self, name: str, categories: list[Category]):
        self.name = name
        self.state = get_starting_state(categories)

    def _display_dice(self):
        print(f'{self.name} rolls: ')
        for idx, dice in enumerate(self.state.dice):
            print(f'Dice {idx + 1}: {dice}')

    def _display_choice(self, dice: list[int], category: Category):
        print(f'{self.name} chose {category.name} with a {dice} roll and scored {self.state.scores[category]} points')

    def _display_player_turn(self):
        print(f'----{self.name}\'s ----')

    def get_score(self):
        return self.state.get_score()

    def get_bonus(self):
        return self.state.get_bonus()

    def handle_rerolls(self):
        pass

    def chose_category(self, joker_rule=False):
        pass

    def play_turn(self):
        pass
