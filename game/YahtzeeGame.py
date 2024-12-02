from player.AiPlayer import AiPlayer
from player.HumanPlayer import HumanPlayer
from player.Player import Player
from state.Category import Category


class YahtzeeGame:
    player1: Player
    player2: Player
    categories: list[Category]

    def __init__(self, categories: list[Category]):
        name = input('Enter your name: ')
        self.player1 = HumanPlayer(name, categories)
        self.player2 = AiPlayer('Opponent', categories)
        self.categories = categories

    def _display_turn_end(self):
        print(f'----Turn ended----')
        print(f'{self.player1.name} score: {self.player1.get_score()}')
        print(f'{self.player2.name} score: {self.player2.get_score()}')

    def _display_winner(self):
        print('----Game ended----')
        if self.player1.get_score() > self.player2.get_score():
            print(f'{self.player1.name} wins!')
        elif self.player1.get_score() < self.player2.get_score():
            print(f'{self.player2.name} wins!')
        else:
            print('It\'s a tie!')

    def _display_categories(self):
        for idx, category in enumerate(self.categories):
            print(f'{idx + 1}. {category.name} - {category.description}')

    def play(self):
        print('----Game started----')
        self._display_categories()
        turn = 0
        while not self.player1.state.is_final() and not self.player2.state.is_final():
            self.player1.play_turn()
            self.player2.play_turn()
            self._display_turn_end()
        self._display_winner()
