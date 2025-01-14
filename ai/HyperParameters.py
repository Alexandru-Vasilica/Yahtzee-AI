from typing_extensions import TypedDict


class Hyperparameters(TypedDict):
    gamma: float
    epsilon: float
    epsilon_min: float
    epsilon_decay: float
    learning_rate: float
    batch_size: int
    episodes: int
    replay_buffer_capacity: int


hyperparameters = Hyperparameters(
    gamma=0.9,
    epsilon=1.0,
    epsilon_min=0.05,
    epsilon_decay=0.00001,
    learning_rate=0.0001,
    batch_size=128,
    episodes=10_000,
    replay_buffer_capacity=100_000
)
