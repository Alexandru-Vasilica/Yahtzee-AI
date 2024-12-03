from state.Category import Category
from player.Player import Player
from state.Action import get_action_from_rerolls,AssignAction
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
        self.chose_category(joker_rule)

    def handle_rerolls(self):
        while self.state.rerolls_left > 0:
            answer = None
            while answer not in ['y', 'n']:
                answer = input("Would you like to reroll some dice? (y/n): ")
            if answer == 'n':
                return
            reroll = input(
                "Which dice would you like to reroll? (Write the number of the dice[1-5] separated by a space): ")
            dice_to_reroll = []
            for dice in reroll.split(' '):
                if dice not in ['1', '2', '3', '4', '5']:
                    print(f'Invalid dice number {dice}')
                    continue
                dice_to_reroll.append(int(dice) - 1)
            print(f'Rerolling dice: {dice_to_reroll}')
            action = get_action_from_rerolls(dice_to_reroll)
            self.state = transition(self.state, action)
            self._display_dice()

    def chose_category(self, joker_rule=False):
        print(f'Available categories: ')
        valid_categories = []
        for idx, category in enumerate(self.state.scores.keys()):
            if self.state.scores.get(category) is not None:
                continue
            print(f'{idx + 1}. {category.name} - Points: {category.get_score(self.state.dice, joker_rule)}')
            valid_categories.append(category.name)
        category_name = None
        while category_name not in valid_categories:
            if category_name is not None:
                print(f'Invalid category: {category_name}')
            category_name = input('Choose a category: ').lstrip().rstrip()
        category = next(category for category in self.state.scores.keys() if category.name == category_name)
        action = AssignAction(category.index)
        old_dice = self.state.dice
        self.state = transition(self.state, action)
        self._display_choice(old_dice, category)
