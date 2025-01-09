from state.Category import Category
from player.Player import Player
from state.Action import get_action_from_rerolls, AssignAction
from state.State import transition
from utils.dice import check_yahtzee


class HumanPlayer(Player):

    def __init__(self, name: str, categories: list[Category]):
        super().__init__(name, categories)

    def play_turn(self):
        self._display_player_turn()
        self._display_dice()
        self.handle_rerolls()
        joker_rule = False
        if check_yahtzee(self.state.dice):
            print('Yahtzee!')
            joker_rule = self.state.yahtzee_count > 0
        self.chose_category(None, joker_rule)

    def handle_rerolls(self, game_answer=None, rerolls=None):
        if self.state.rerolls_left <= 0:
            return

        answer = game_answer if game_answer else input("Would you like to reroll some dice? (y/n): ")
        if answer == 'n':
            return

        if rerolls is None:
            reroll = input(
                "Which dice would you like to reroll? (Write the number of the dice[1-5] separated by a space): ")
            dice_to_reroll = [int(d) - 1 for d in reroll.split() if d in ['1', '2', '3', '4', '5']]
        else:
            dice_to_reroll = rerolls

        action = get_action_from_rerolls(dice_to_reroll)
        self.state = transition(self.state, action)
        self._display_dice()

    def chose_category(self, name=None, joker_rule=False):
        print(f'Available categories: ')
        valid_categories = []
        for idx, category in enumerate(self.state.scores.keys()):
            if self.state.scores.get(category) is not None:
                continue
            print(f'{idx + 1}. {category.name} - Points: {category.get_score(self.state.dice, joker_rule)}')
            valid_categories.append(category.name)
        category_name = name
        while category_name not in valid_categories:
            if category_name is not None:
                print(f'Invalid category: {category_name}')
            category_name = input('Choose a category: ').lstrip().rstrip()
        category = next(category for category in self.state.scores.keys() if category.name == category_name)
        old_dice = self.state.dice
        action = AssignAction(category.index)
        self.state = transition(self.state, action)
        self._display_choice(old_dice, category)