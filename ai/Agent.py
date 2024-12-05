import pickle
from collections import defaultdict

import numpy as np

from ai import HyperParameters
from state.Action import Action, get_action_from_index, ACTION_SIZE
from state.Category import Category, categories
from state.State import State, get_starting_state, transition


class Agent:
    q_table: dict[State, np.ndarray]
    alpha: float
    gamma: float
    epsilon: float
    state: State

    def __init__(self, action_size: int, hyperparameters: HyperParameters, categories: list[Category]):
        self.q_table = defaultdict(lambda: np.zeros(action_size))
        self.alpha = hyperparameters['alpha']
        self.gamma = hyperparameters['gamma']
        self.epsilon = hyperparameters['epsilon']
        self.state = get_starting_state(categories)

    def choose_action(self) -> Action:
        valid_actions = self.state.get_valid_actions()
        if np.random.rand() < self.epsilon:
            action = valid_actions[np.random.randint(0, len(valid_actions))]
        else:
            q_values = {action: self.q_table[self.state][action.index] for action in valid_actions}
            action = max(q_values, key=q_values.get)
        return action

    def update(self, action: Action):
        next_state = transition(self.state, action)
        reward = next_state.get_score() - self.state.get_score()
        if next_state.is_final():
            td_target = reward
        else:
            next_valid_actions = next_state.get_valid_actions()
            nex_action_outcomes = {action: self.q_table[next_state][action.index] for action in next_valid_actions}
            best_next_action = max(nex_action_outcomes, key=nex_action_outcomes.get)
            td_target = reward + self.gamma * self.q_table[next_state][best_next_action.index]
        td_error = td_target - self.q_table[self.state][action.index]
        self.q_table[self.state][action.index] += self.alpha * td_error
        self.state = next_state
        return reward

    def save(self, path: str):
        with open(path, 'wb') as file:
            try:
                pickle.dump(self.q_table, file)
            except Exception as e:
                print(f'Error saving model: {e}')

    def display_table(self):
        for state, q_values in self.q_table.items():
            print(f'State: {state}')
            print(f'Q-Values: {q_values}')

    def evaluate_agent(self, episodes: int):
        visited_states = len(self.q_table.keys())
        return visited_states


def train_agent(hyperparameters: HyperParameters):
    agent = Agent(ACTION_SIZE, hyperparameters, categories)
    for episode in range(hyperparameters['episodes']):
        agent.state.reset()
        total_reward = 0
        while not agent.state.is_final():
            action = agent.choose_action()
            reward = agent.update(action)
            total_reward += reward
        print(f'Episode {episode + 1}/{hyperparameters["episodes"]} - Total Score: {agent.state.get_score()}')
        # if (episode + 1) % 5 == 0:
        #     agent.save('model.pkl')
    print(f'Average score: {agent.evaluate_agent(hyperparameters["episodes"])}')
