import itertools
import random
import time

from ai.Agent import QLearningAgent
from state.Action import Action, get_action_from_index, ASSIGN_ACTION_BOUNDARY, get_action_from_rerolls
from state.Category import categories
from state.State import State, transition, get_starting_state
from utils.dice import check_yahtzee


class Strategy:
    def __init__(self):
        pass

    def choose_action(self, state: State) -> Action:
        pass


class AgentStrategy(Strategy):
    agent: QLearningAgent

    def __init__(self, path: str):
        super().__init__()
        self.agent = QLearningAgent()
        self.agent.load(path)
        self.agent.mode = 'eval'

    def choose_action(self, state: State) -> Action:
        action_index = self.agent.choose_action(state)
        return get_action_from_index(action_index)


class MinMaxStrategy(Strategy):
    depth: int

    def __init__(self, depth: int):
        super().__init__()
        self.max_player_action = None
        self.depth = depth

    def choose_action(self, state: State) -> Action:
        score, action = self.minmax(state, self.depth, float('-inf'), float('inf'), True)
        return action

    @staticmethod
    def _evaluate_state(state: State) -> float:
        score = state.get_score()

        return score

    def minmax(self, state: State, depth: int, alpha: float, beta: float, is_max_player: bool) -> tuple[
        float, Action | None]:
        if depth == 0 or state.is_final():
            return self._evaluate_state(state), None
        if is_max_player:
            eval, action = self._max_player_turn(state, depth, alpha, beta)
            return eval, action
        else:
            return self._chance_player_turn(state, depth, alpha, beta)

    def _max_player_turn(self, state: State, depth: int, alpha: float, beta: float):
        max_eval = float('-inf')
        best_action = None

        for action in state.get_valid_actions():
            new_state = transition(state, action)
            self.max_player_action = action
            eval_score, _ = self.minmax(new_state, depth - 1, alpha, beta,
                                        True if action.index <= ASSIGN_ACTION_BOUNDARY else False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        self.max_player_action = best_action
        return max_eval, best_action

    def _chance_player_turn(self, state: State, depth: int, alpha: float, beta: float):
        total_eval = 0
        count = 0

        max_player_action = self.max_player_action
        if max_player_action.index <= ASSIGN_ACTION_BOUNDARY or state.rerolls_left == 0:
            return self.minmax(state, depth - 1, alpha, beta, True)
        rerolls = max_player_action.rerolls
        for _ in range(20):
            action = get_action_from_rerolls(rerolls)
            new_state = transition(state, action)
            eval_score, _ = self.minmax(new_state, depth - 1, alpha, beta, True)
            total_eval += eval_score
            count += 1

            average = total_eval / count
            beta = min(beta, average)
            if beta <= alpha and count > 8:
                break
        expected_value = total_eval / count
        return expected_value, None


def run_strategy(strategy: Strategy):
    state = get_starting_state(categories=categories)
    while not state.is_final():
        action = strategy.choose_action(state)
        state = transition(state, action)
    return state.get_score()


def test_strategy(strategy: Strategy, runs: int):
    start = time.time()
    scores = []
    for _ in range(runs):
        score = run_strategy(strategy)
        scores.append(score)
    end = time.time()
    print(f'Average score: {sum(scores) / runs}')
    print('Max score: ', max(scores))
    print(f'Total time: {end - start}')
    print(f'Average time: {(end - start) / runs}')


