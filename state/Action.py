ASSIGN_ACTION_BOUNDARY: int = 12
ACTION_SIZE: int = 32 + ASSIGN_ACTION_BOUNDARY


class Action:
    index: int

    def __init__(self, index: int):
        self.index = index

    def __hash__(self):
        return self.index


class RerollAction(Action):
    rerolls: list[int]

    def __init__(self, index: int):
        super().__init__(index)
        self.rerolls = []
        index = index - 12
        for i in range(5):
            if index & (1 << i):
                self.rerolls.append(i)


class AssignAction(Action):

    def __init__(self, index: int):
        super().__init__(index)


def get_action_from_index(index: int) -> Action:
    if index <= ASSIGN_ACTION_BOUNDARY:
        return AssignAction(index)
    return RerollAction(index)


def get_action_from_rerolls(rerolls: list[int]) -> RerollAction:
    index = 0
    for i in rerolls:
        index |= 1 << i
    return RerollAction(index + ASSIGN_ACTION_BOUNDARY)
