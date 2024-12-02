import numpy as np
import random
from collections import defaultdict


# Utility Functions
def roll_dice():
    """Rolls 5 six-sided dice."""
    return sorted([random.randint(1, 6) for _ in range(5)])


def reroll_dice(dice, reroll_indices):
    """Rerolls selected dice indices."""
    return sorted([random.randint(1, 6) if i in reroll_indices else d for i, d in enumerate(dice)])


# Yahtzee Simulator
class YahtzeeEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dice = roll_dice()
        self.rerolls_left = 2
        self.scorecard = {cat: None for cat in self.categories()}
        return self.get_state()

    def categories(self):
        """List of Yahtzee scoring categories."""
        return ['Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
                'ThreeOfAKind', 'FourOfAKind', 'FullHouse',
                'SmallStraight', 'LargeStraight', 'Yahtzee', 'Chance']

    def valid_actions(self):
        """Returns valid actions based on rerolls and scorecard state."""
        actions = []
        if self.rerolls_left > 0:
            actions += [f"Reroll:{i}" for i in range(1, 32)]  # 31 subsets for reroll
        for category, score in self.scorecard.items():
            if score is None:
                actions.append(f"Score:{category}")
        return actions

    def calculate_score(self, category):
        """Calculate score for a category based on current dice."""
        dice = self.dice
        if category == 'Aces':
            return sum(d for d in dice if d == 1)
        elif category == 'Twos':
            return sum(d for d in dice if d == 2)
        elif category == 'Threes':
            return sum(d for d in dice if d == 3)
        elif category == 'Fours':
            return sum(d for d in dice if d == 4)
        elif category == 'Fives':
            return sum(d for d in dice if d == 5)
        elif category == 'Sixes':
            return sum(d for d in dice if d == 6)
        elif category == 'ThreeOfAKind' and len(set(dice)) <= 3:
            return sum(dice)
        elif category == 'FourOfAKind' and len(set(dice)) <= 2:
            return sum(dice)
        elif category == 'FullHouse' and len(set(dice)) == 2:
            return 25
        elif category == 'SmallStraight' and set(dice).issuperset({1, 2, 3, 4}) or \
                set(dice).issuperset({2, 3, 4, 5}) or \
                set(dice).issuperset({3, 4, 5, 6}):
            return 30
        elif category == 'LargeStraight' and set(dice) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
            return 40
        elif category == 'Yahtzee' and len(set(dice)) == 1:
            return 50
        elif category == 'Chance':
            return sum(dice)
        return 0

    def step(self, action):
        """Execute an action and return the next state, reward, and done."""
        if action.startswith("Reroll"):
            reroll_mask = int(action.split(":")[1])
            indices = [i for i in range(5) if reroll_mask & (1 << i)]
            self.dice = reroll_dice(self.dice, indices)
            self.rerolls_left -= 1
            return self.get_state(), 0, False
        elif action.startswith("Score"):
            category = action.split(":")[1]
            score = self.calculate_score(category)
            self.scorecard[category] = score
            done = all(v is not None for v in self.scorecard.values())
            return self.get_state(), score, done

    def get_state(self):
        """Encodes the environment state as a tuple."""
        return tuple(self.dice), self.rerolls_left, tuple(self.scorecard.values())


# RL Agent
class YahtzeeAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(action_size))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.state_size = state_size
        self.action_size = action_size

    def choose_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        q_values = {action: self.q_table[state][idx] for idx, action in enumerate(valid_actions)}
        return max(q_values, key=q_values.get)

    def update(self, state, action_idx, reward, next_state, valid_next_actions):
        best_next_action = np.argmax([self.q_table[next_state][i] for i in range(len(valid_next_actions))])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action_idx]
        self.q_table[state][action_idx] += self.alpha * td_error


# Training Loop
def train_yahtzee_agent(episodes=1000):
    env = YahtzeeEnvironment()
    agent = YahtzeeAgent(state_size=13 + 5 + 1, action_size=44)

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0

        while True:
            valid_actions = env.valid_actions()
            action = agent.choose_action(state, valid_actions)
            next_state, reward, done = env.step(action)

            action_idx = valid_actions.index(action)
            next_valid_actions = env.valid_actions()
            agent.update(state, action_idx, reward, next_state, next_valid_actions)

            state = next_state
            total_reward += reward

            if done:
                break

        print(f"Episode {episode + 1}/{episodes} - Total Score: {total_reward}")


# Run Training
train_yahtzee_agent(episodes=1000)
