import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

from state.Action import ACTION_SIZE
from state.State import State

device = torch.device("cpu")

INPUT_DIM = 23
OUTPUT_DIM = ACTION_SIZE


class QNetwork(nn.Module):
    def __init__(self):
        super(QNetwork, self).__init__()
        self.l1 = nn.Linear(INPUT_DIM, 64)
        self.l2 = nn.Linear(64, 128)
        self.l3 = nn.Linear(128, 64)
        self.l4 = nn.Linear(64, OUTPUT_DIM)

        nn.init.xavier_uniform_(self.l1.weight)
        nn.init.xavier_uniform_(self.l2.weight)
        nn.init.xavier_uniform_(self.l3.weight)
        nn.init.xavier_uniform_(self.l4.weight)

        self.to(device)

    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
        x = x.to(device)

        x = torch.relu(self.l1(x))
        x = torch.relu(self.l2(x))
        x = torch.relu(self.l3(x))
        x = self.l4(x)
        return x


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


class QLearningAgent:
    def __init__(self, gamma=0.9, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.00001,
                 lr=0.00025, replay_buffer_capacity=50000):
        self.input_dim = INPUT_DIM
        self.output_dim = OUTPUT_DIM
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_network = QNetwork()
        self.target_network = QNetwork()
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=replay_buffer_capacity)
        self.mode = 'train'
        self.steps = 0

    def choose_action(self, state: State):
        valid_actions = [action.index for action in state.get_valid_actions()]
        if np.random.rand() < self.epsilon and self.mode == 'train':
            return np.random.choice(valid_actions)
        state_tensor = torch.FloatTensor(state.to_features()).to(device)
        q_values = self.q_network(state_tensor).squeeze(0)
        mask = torch.full_like(q_values, float('-inf'))
        mask[valid_actions] = 0
        q_values = q_values + mask
        return torch.argmax(q_values).item()

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def train(self, batch_size):
        if len(self.replay_buffer) < batch_size:
            return
        batch = self.replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = np.array(states)
        next_states = np.array(next_states)
        states = torch.FloatTensor(states).to(device)
        actions = torch.LongTensor(actions).to(device)
        rewards = torch.FloatTensor(rewards).to(device)
        next_states = torch.FloatTensor(next_states).to(device)
        dones = torch.FloatTensor(dones).to(device)

        q_values = self.q_network(states)

        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]

            target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = nn.MSELoss()(q_values, target_q_values.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps += 1
        if self.steps % 100 == 0:
            self.update_target_network()

        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay

    def save(self, filepath):
        state = {
            'q_network_state_dict': self.q_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'epsilon_min': self.epsilon_min,
            'epsilon_decay': self.epsilon_decay,
        }
        torch.save(state, filepath)
        print(f"Agent saved to {filepath}")

    def load(self, filepath):
        state = torch.load(filepath)
        self.q_network.load_state_dict(state['q_network_state_dict'])
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.optimizer.load_state_dict(state['optimizer_state_dict'])
        self.epsilon = state['epsilon']
        self.epsilon_min = state['epsilon_min']
        self.epsilon_decay = state['epsilon_decay']
        print(f"Agent loaded from {filepath}")
