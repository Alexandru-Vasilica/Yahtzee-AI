import pickle
from collections import defaultdict
import numpy as np

from state.Action import Action, get_action_from_index, ACTION_SIZE, ASSIGN_ACTION_BOUNDARY
from state.Category import Category, categories
from state.State import State, get_starting_state, transition

OPPORTUNITY_MULTIPLIER = 5


class QTableSerializer:
    @staticmethod
    def save(q_table: dict[State, np.ndarray], path: str):
        try:
            serializable_q_table = dict(q_table)
            with open(path, 'wb') as file:
                pickle.dump(serializable_q_table, file)
            print(f"Q-table successfully saved to {path}")
        except Exception as e:
            print(f"Error saving Q-table: {e}")

    @staticmethod
    def load(path: str) -> dict[State, np.ndarray]:
        try:
            with open(path, 'rb') as file:
                q_table = pickle.load(file)
            print(f"Q-table successfully loaded from {path}")
            return defaultdict(lambda: np.zeros(ACTION_SIZE), q_table)
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            return defaultdict(lambda: np.zeros(ACTION_SIZE))


class YahtzeeEnvironment:
    state: State

    def __init__(self, categories: list[Category]):
        self.state = get_starting_state(categories)

    @staticmethod
    def _calculate_reward(previous_state: State, next_state: State, action: Action) -> int:
        if action.index <= ASSIGN_ACTION_BOUNDARY:
            score_gained = next_state.get_score() - previous_state.get_score()
            category = next(category for category in categories if category.index == action.index)
            return score_gained - category.max_score/2
        else:
            old_potential_score = previous_state.get_potential_score()
            new_potential_score = next_state.get_potential_score()

            old_opportunities = previous_state.get_scoring_opportunities()
            new_opportunities = next_state.get_scoring_opportunities()

            return (new_potential_score - old_potential_score) + (
                    new_opportunities - old_opportunities) * OPPORTUNITY_MULTIPLIER

    def step(self, action: Action) -> tuple[State, int, bool, dict]:
        next_state = transition(self.state, action)
        reward = self._calculate_reward(self.state, next_state, action)
        done = next_state.is_final()
        info = {}
        if done:
            info['score'] = next_state.get_score()
        self.state = next_state
        return next_state, reward, done, info

    def reset(self) -> State:
        self.state = get_starting_state(categories)
        return self.state


