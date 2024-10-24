from game.Category import Category
from player.Player import Player


class HumanPlayer(Player):

    def __init__(self, name: str, categories: list[Category]):
        super().__init__(name, categories)

    def play_turn(self):
        self._display_player_turn()
        self.roll_dice(list(range(5)))
        self.handle_rerolls()
        is_yahtzee = self.verify_yahtzee()
        joker_rule = False
        if is_yahtzee:
            joker_rule = self.handle_yahtzee()
        self.chose_category(joker_rule)
        self.reset_dice()

    def handle_rerolls(self):
        for _ in range(2):
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
            self.roll_dice(dice_to_reroll)

    def chose_category(self, joker_rule=False):
        print(f'Available categories: ')
        valid_categories = []
        for idx, category in enumerate(self.scorecard.keys()):
            if self.scorecard.get(category) is not None:
                continue
            print(f'{idx + 1}. {category.name} - Points: {category.get_score(self.dice, joker_rule)}')
            valid_categories.append(category.name)
        category_name = None
        while category_name not in valid_categories:
            if category_name is not None:
                print(f'Invalid category: {category_name}')
            category_name = input('Choose a category: ').lstrip().rstrip()
        category = next(category for category in self.scorecard.keys() if category.name == category_name)
        self.check_scorecard(category, joker_rule)
        self._display_choice(category)