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

    # def choose_action(self) -> Action:
    #     valid_actions = self.state.get_valid_actions()
    #     if np.random.rand() < self.epsilon:
    #         action_index = np.random.choice(len(valid_actions))
    #         action = valid_actions[action_index]
    #     else:
    #         q_values = np.array([self.q_table[self.state][action.index] for action in valid_actions])
    #         best_action_index = np.argmax(q_values)
    #         action = valid_actions[best_action_index]
    #     return action

    def step(self, action: Action) -> tuple[State, int, bool, dict]:
        next_state = transition(self.state, action)
        reward = self._calculate_reward(self.state, next_state, action)
        done = next_state.is_final()
        info = {}
        if done:
            info['score'] = next_state.get_score()
        # if next_state.is_final():
        #     td_target = reward
        # else:
        #     next_valid_actions = next_state.get_valid_actions()
        #     nex_action_outcomes = {action: self.q_table[next_state][action.index] for action in next_valid_actions}
        #     best_next_action = max(nex_action_outcomes, key=nex_action_outcomes.get)
        #     td_target = reward + self.gamma * self.q_table[next_state][best_next_action.index]
        # td_error = td_target - self.q_table[self.state][action.index]
        # self.q_table[self.state][action.index] += self.alpha * td_error
        self.state = next_state
        return next_state, reward, done, info

    def reset(self) -> State:
        self.state = get_starting_state(categories)
        return self.state

    # def display_table(self):
    #     for state, q_values in self.q_table.items():
    #         print(f"State: {state}")
    #         print(f"Q-Values: {q_values}")

    # def evaluate_agent(self, episodes: int):
    #     visited_states = len(self.q_table.keys())
    #     return visited_states

    # def save_q_table(self, path: str):
    #     QTableSerializer.save(self.q_table, path)

    # def load_q_table(self, path: str):
    #     self.q_table = QTableSerializer.load(path)

    # def display_policy(self):
    #     print("Optimal Policy:")
    #     for state, q_values in self.q_table.items():
    #         best_action_index = int(np.argmax(q_values))
    #         best_action = get_action_from_index(best_action_index)
    #         print(f"State: {state} -> Best Action: {best_action}")

# def train_agent(hyperparameters: HyperParameters):
#     agent = Agent(ACTION_SIZE, hyperparameters, categories)
#     rewards_per_episode = []
#     for episode in range(hyperparameters['episodes']):
#         agent.state.reset()
#         total_reward = 0
#         while not agent.state.is_final():
#             action = agent.choose_action()
#             reward = agent.update(action)
#             total_reward += reward
#         rewards_per_episode.append(total_reward)
#         if (episode + 1) % 50000 == 0:
#             agent.save_q_table("q_table150k.pkl")
#             print(f'Episode {episode + 1}/{hyperparameters["episodes"]} - Total Score: {agent.state.get_score()}')
#         agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
#
#     print(f'Average score: {agent.evaluate_agent(hyperparameters["episodes"])}')
#     plt.plot(range(1, hyperparameters['episodes'] + 1), rewards_per_episode)
#     plt.xlabel('Episode')
#     plt.ylabel('Total Reward')
#     plt.title('Convergence of Q-Learning')
#     plt.savefig('chart.png')
#     plt.show()
