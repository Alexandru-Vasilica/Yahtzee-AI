from typing import TypedDict


class Category:
    name: str
    description: str

    def get_score(self,dice:list[int]) -> int:
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Sum(Category):

    def __init__(self):
        self.name = 'Sum'
        self.description = 'Sum of all dice'
    def get_score(self, dice: list[int]) -> int:
        return sum(dice)

class Ones(Category):

    def __init__(self):
        self.name = 'Ones'
        self.description = 'Sum of all ones'
    def get_score(self, dice: list[int]) -> int:
        return dice.count(1)