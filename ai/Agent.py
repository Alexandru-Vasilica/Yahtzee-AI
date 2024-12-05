import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

from ai import HyperParameters
from state.Action import Action, get_action_from_index, ACTION_SIZE
from state.Category import Category, categories
from state.State import State, get_starting_state, transition


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
        self.epsilon = hyperparameters['epsilon_start']
        self.epsilon_min = hyperparameters['epsilon_min']
        self.epsilon_decay = hyperparameters['epsilon_decay']
        self.state = get_starting_state(categories)

    def choose_action(self) -> Action:
        valid_actions = self.state.get_valid_actions()
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(len(valid_actions))
            action = valid_actions[action_index]
        else:
            q_values = np.array([self.q_table[self.state][action.index] for action in valid_actions])
            best_action_index = np.argmax(q_values)
            action = valid_actions[best_action_index]
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

    def display_table(self):
        for state, q_values in self.q_table.items():
            print(f"State: {state}")
            print(f"Q-Values: {q_values}")

    def evaluate_agent(self, episodes: int):
        visited_states = len(self.q_table.keys())
        return visited_states

    def save_q_table(self, path: str):
        QTableSerializer.save(self.q_table, path)

    def load_q_table(self, path: str):
        self.q_table = QTableSerializer.load(path)

    def display_policy(self):
        print("Optimal Policy:")
        for state, q_values in self.q_table.items():
            best_action_index = int(np.argmax(q_values))
            best_action = get_action_from_index(best_action_index)
            print(f"State: {state} -> Best Action: {best_action}")


def train_agent(hyperparameters: HyperParameters):
    agent = Agent(ACTION_SIZE, hyperparameters, categories)
    rewards_per_episode = []
    for episode in range(hyperparameters['episodes']):
        agent.state.reset()
        total_reward = 0
        while not agent.state.is_final():
            action = agent.choose_action()
            reward = agent.update(action)
            total_reward += reward
        rewards_per_episode.append(total_reward)
        print(f'Episode {episode + 1}/{hyperparameters["episodes"]} - Total Score: {agent.state.get_score()}')
        if (episode + 1) % 5 == 0:
            agent.save_q_table("q_table.pkl")
        agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)

    print(f'Average score: {agent.evaluate_agent(hyperparameters["episodes"])}')
    plt.plot(range(1, hyperparameters['episodes'] + 1), rewards_per_episode)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Convergence of Q-Learning')
    plt.show()
