from os import path

from ai.Agent import QLearningAgent
from ai.Environment import YahtzeeEnvironment
from ai.HyperParameters import hyperparameters
from ai.train import save_path, evaluate_agent
from state.Category import categories

env = YahtzeeEnvironment(categories=categories)

agent = QLearningAgent(gamma=hyperparameters['gamma'], epsilon=hyperparameters['epsilon'],
                       epsilon_min=hyperparameters['epsilon_min'], epsilon_decay=hyperparameters['epsilon_decay'],
                       lr=hyperparameters['learning_rate'],
                       replay_buffer_capacity=hyperparameters['replay_buffer_capacity'])
agent.load(path.join("../agents", "agent_2_1000.pth"))
evaluate_agent(agent, env, num_episodes=100, detailed=True)

