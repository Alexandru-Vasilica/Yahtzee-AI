from typing import TypedDict


class HyperParameters(TypedDict):
    alpha: float
    gamma: float
    epsilon: float
    episodes: int


