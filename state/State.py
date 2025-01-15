from __future__ import annotations

from typing import Dict, Any

from state import Category, Action
from state.Action import get_action_from_index, ASSIGN_ACTION_BOUNDARY
from state.Category import DiceValueCategory
from utils.dice import roll_dice
import numpy as np

UPPER_SECTION_BONUS_BOUNDARY = 63


def check_yahtzee(dice: list[int]) -> bool:
    return len(set(dice)) == 1


class State:
    scores: dict[Category, int | None]
    yahtzee_count: int
    dice: list[int]
    rerolls_left: int

    def __init__(self, scores: dict[Category, int | None], yahtzee_count: int, dice: list[int], rerolls_left: int):
        self.scores = scores
        self.yahtzee_count = yahtzee_count
        self.dice = dice
        self.rerolls_left = rerolls_left

    def reset(self):
        for category in self.scores.keys():
            self.scores[category] = None
        self.yahtzee_count = 0
        self.dice = roll_dice(self.dice, [0, 1, 2, 3, 4])
        self.rerolls_left = 2

    def init(self):
        self.dice = roll_dice(self.dice, [0, 1, 2, 3, 4])
        self.rerolls_left = 2

    def is_final(self):
        for category in self.scores.keys():
            if self.scores[category] is None:
                return False
        return True

    def get_bonus(self):
        bonus = 0
        score = 0
        for category in self.scores.keys():
            if isinstance(category, DiceValueCategory) and self.scores[category] is not None:
                score += self.scores[category]
        if score >= UPPER_SECTION_BONUS_BOUNDARY:
            bonus = 35
        yahtzee_bonus = 0 if self.yahtzee_count == 0 else (self.yahtzee_count - 1) * 100
        return bonus + yahtzee_bonus

    def get_score(self):
        return sum([score for score in self.scores.values() if score is not None]) + self.get_bonus()

    def get_valid_actions(self):
        actions = []
        for category in self.scores.keys():
            if self.scores[category] is None:
                actions.append(get_action_from_index(category.index))
        if self.rerolls_left > 0:
            for i in range(1, 32):
                actions.append(get_action_from_index(ASSIGN_ACTION_BOUNDARY + i))
        return actions

    def get_scoring_opportunities(self) -> int:
        return len([category for category in self.scores.keys() if category.get_score(self.dice) > 0])

    def get_potential_score(self) -> int:
        potential_score = []
        for category in self.scores.keys():
            if self.scores[category] is None:
                action = get_action_from_index(category.index)
                potential_state = transition(self, action)
                potential_score.append(potential_state.get_score() - self.get_score())
        return max(potential_score, default=0)

    def __hash__(self):
        return hash((tuple(score is not None for score in self.scores.values()), tuple(self.dice), self.rerolls_left))

    def _scores_to_string(self):
        return ', '.join([f'{category.name}: {score}' for category, score in self.scores.items()])

    def __str__(self):
        return f'State(scores={self._scores_to_string()}, yahtzee_count={self.yahtzee_count}, dice={self.dice}, rerolls_left={self.rerolls_left})'

    def to_features(self) -> np.ndarray:
        """
        Converts the state to a feature vector containing the following features:
        - 13 features for each category (1 if the category is not scored yet, 0 otherwise)
        - 6 features for each dice value (number of dice with the value normalized by 5)
        - 1 feature for the number of rerolls left (normalized by 2)
        - 1 feature for the upper section score (normalized by 63)
        - 1 feature for the number of remaining upper section categories (normalized by 6)
        - 1 feature for the Yahtzee feature (1 if the dice is a Yahtzee, 0 otherwise)
        :return: a numpy array containing 23 features
        """
        features = []
        for category in self.scores.keys():
            features.append(1 if self.scores[category] is not None else 0)
        dice_features = [0] * 6
        for die in self.dice:
            dice_features[die - 1] += 1
        features.extend([value / 5 for value in dice_features])
        features.append(self.rerolls_left / 2)
        upper_section_score = 0
        for category in self.scores.keys():
            if isinstance(category, DiceValueCategory) and self.scores[category] is not None:
                upper_section_score += self.scores[category]
        remaining_upper_section_categories = len([category for category in self.scores.keys() if
                                                  isinstance(category, DiceValueCategory) and self.scores[
                                                      category] is None])
        features.append(upper_section_score / UPPER_SECTION_BONUS_BOUNDARY)
        features.append(remaining_upper_section_categories / 6)
        yahtzee_feature = 1 if check_yahtzee(self.dice) else 0
        features.append(yahtzee_feature)
        return np.array(features, dtype=np.float32)


def get_starting_state(categories: list[Category]) -> State:
    scores = {}
    for category in categories:
        scores[category] = None
    return State(scores=scores, yahtzee_count=0, dice=roll_dice([0, 0, 0, 0, 0], [0, 1, 2, 3, 4]), rerolls_left=2)


def transition(state: State, action) -> State:
    new_yahtzee_count: int = state.yahtzee_count
    new_scores: dict[Any, int | None] = state.scores.copy()
    if action.index <= ASSIGN_ACTION_BOUNDARY:
        category = next(category for category in state.scores.keys() if category.index == action.index)
        joker_rule = False
        if check_yahtzee(state.dice) and (category.name == 'Yahtzee' or new_yahtzee_count > 0):
            new_yahtzee_count += 1
            joker_rule = new_yahtzee_count > 1
        new_scores[category] = category.get_score(state.dice, joker_rule)
        return State(new_scores, new_yahtzee_count, roll_dice(state.dice, [0, 1, 2, 3, 4]), 2)
    else:
        new_dice = roll_dice(state.dice, action.rerolls)
        return State(new_scores, new_yahtzee_count, new_dice, state.rerolls_left - 1)
