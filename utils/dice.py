import numpy


def roll_dice(dice: list[int], rolls: list[int]) -> list[int]:
    new_dice = dice.copy()
    for i in rolls:
        new_dice[i] = numpy.random.randint(1, 7)
    return new_dice


def check_yahtzee(dice: list[int]) -> bool:
    return len(set(dice)) == 1
