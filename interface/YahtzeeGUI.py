import tkinter as tk
from tkinter import messagebox

from game.YahtzeeGame import YahtzeeGame
from player.HumanPlayer import HumanPlayer


class YahtzeeGUI:
    def __init__(self, root, categories):
        self.start_button = None
        self.player1_name_entry = None
        self.player1_name_label = None
        self.categories = categories
        self.root = root
        self.game = None
        self.current_player = None
        self.turn_phase = "roll"
        self.reroll_count = 0
        self.valid_categories = [category.name for category in categories]

        self.root.title("Yahtzee Game")

        self.score_frame = None
        self.player1_score = None
        self.player2_score = None
        self.dice_frame = None
        self.dice_buttons = []
        self.roll_button = None
        self.category_frame = None
        self.category_buttons = []
        self.action_label = None
        self.reroll_button = None
        self.skip_reroll_button = None

        self.setup_name_entry()

    def setup_name_entry(self):
        name_frame = tk.Frame(self.root)
        name_frame.pack(side=tk.TOP, pady=20)

        self.player1_name_label = tk.Label(name_frame, text="Enter Player 1 Name:")
        self.player1_name_label.pack(side=tk.LEFT, padx=5)
        self.player1_name_entry = tk.Entry(name_frame)
        self.player1_name_entry.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.TOP, pady=20)

    def start_game(self):
        player1_name = self.player1_name_entry.get()
        self.game = YahtzeeGame(player1_name, self.categories)
        self.current_player = self.game.player1

        self.player1_name_label.pack_forget()
        self.player1_name_entry.pack_forget()
        self.start_button.pack_forget()
        self.setup_ui()

    def setup_ui(self):
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(side=tk.TOP, fill=tk.X)
        self.player1_score = tk.Label(self.score_frame, text=f"{self.game.player1.name}: 0")
        self.player1_score.pack(side=tk.LEFT, padx=20)
        self.player2_score = tk.Label(self.score_frame, text=f"{self.game.player2.name}: 0")
        self.player2_score.pack(side=tk.RIGHT, padx=20)

        self.dice_frame = tk.Frame(self.root)
        self.dice_frame.pack(side=tk.TOP, pady=20)
        self.dice_buttons = [
            tk.Button(self.dice_frame, text=f"Dice {i + 1}: ?", width=10, state=tk.DISABLED, command=lambda idx=i: self.toggle_dice_selection(idx))
            for i in range(5)
        ]
        for btn in self.dice_buttons:
            btn.pack(side=tk.LEFT, padx=5)

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.handle_turn)
        self.roll_button.pack(side=tk.TOP, pady=10)

        self.reroll_button = tk.Button(self.root, text="Reroll Selected Dice", command=self.reroll_dice, state=tk.DISABLED)
        self.reroll_button.pack(side=tk.TOP, pady=5)
        self.skip_reroll_button = tk.Button(self.root, text="Keep Dice and Choose Category", command=self.skip_reroll, state=tk.DISABLED)
        self.skip_reroll_button.pack(side=tk.TOP, pady=5)

        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(side=tk.TOP, pady=10)
        self.category_buttons = [
            tk.Button(
                self.category_frame,
                text=category.name,
                command=lambda c=category: self.choose_category(c),
                state=tk.DISABLED,
            )
            for category in self.game.categories
        ]
        for btn in self.category_buttons:
            btn.pack(side=tk.LEFT, padx=5)

        self.action_label = tk.Label(self.root, text=f"{self.current_player.name}'s turn! Roll the dice.")
        self.action_label.pack(side=tk.TOP, pady=20)

        self.start_turn()

    def start_turn(self):
        self.turn_phase = "roll"
        self.reroll_count = 0
        self.action_label.config(text=f"{self.current_player.name}'s turn! Roll the dice.")
        if isinstance(self.current_player, HumanPlayer):
            self.roll_button.config(state=tk.NORMAL)
        else:
            self.disable_category_selection()
            self.handle_turn()

    def handle_turn(self):
        if self.turn_phase == "roll":
            self.current_player.state.init()
            self.update_dice_display()
            self.turn_phase = "reroll"
            self.action_label.config(text=f"{self.current_player.name}'s turn! Deciding to reroll or choose a category.")
            self.roll_button.config(state=tk.DISABLED)

            if isinstance(self.current_player, HumanPlayer):
                self.enable_category_selection()
                self.enable_reroll_options()
            else:
                self.execute_ai_decision()

    def execute_ai_decision(self):
        self.turn_phase = "choose_category"
        self.action_label.config(text=f"{self.current_player.name} is choosing a category.")
        self.current_player.chose_category()
        self.update_scores()
        self.switch_turn()

    def reroll_dice(self):
        self.enable_reroll_options()
        selected_indices = self.get_selected_dice_indices()
        self.current_player.handle_rerolls('y', selected_indices)
        self.update_dice_display()
        self.reroll_count += 1
        print(f"Reroll count: {self.reroll_count}")

        if self.reroll_count == 2:
            self.disable_reroll_options()
            self.enable_category_selection()
            self.action_label.config(text=f"{self.current_player.name}, choose a category.")
        else:
            self.action_label.config(text=f"{self.current_player.name}'s turn! Reroll the dice.")

    def skip_reroll(self):
        self.turn_phase = "choose_category"
        self.disable_reroll_options()
        self.enable_category_selection()
        self.action_label.config(text=f"{self.current_player.name}, choose a category.")

    def toggle_dice_selection(self, idx):
        btn = self.dice_buttons[idx]
        current_text = btn["text"]
        if "SELECTED" in current_text:
            btn.config(text=current_text.replace(" SELECTED", ""))
        else:
            btn.config(text=current_text + " SELECTED")

    def enable_reroll_options(self):
        self.reroll_button.config(state=tk.NORMAL)
        self.skip_reroll_button.config(state=tk.NORMAL)
        self.enable_dice_selection()

    def disable_reroll_options(self):
        self.reroll_button.config(state=tk.DISABLED)
        self.skip_reroll_button.config(state=tk.DISABLED)
        for btn in self.dice_buttons:
            btn.config(state=tk.DISABLED)

    def enable_dice_selection(self):
        for btn in self.dice_buttons:
            btn.config(state=tk.NORMAL)

    def get_selected_dice_indices(self):
        return [idx for idx, btn in enumerate(self.dice_buttons) if "SELECTED" in btn["text"]]

    def update_dice_display(self):
        for idx, dice_value in enumerate(self.current_player.state.dice):
            btn = self.dice_buttons[idx]
            btn.config(state=tk.NORMAL, text=f"Dice {idx + 1}: {dice_value}")

    def enable_category_selection(self):
        for btn in self.category_buttons:
            if btn["text"] in self.valid_categories:
                btn.config(state=tk.NORMAL)

    def disable_category_selection(self):
        for btn in self.category_buttons:
            btn.config(state=tk.DISABLED)

    def choose_category(self, category):
        if category.name in self.valid_categories:
            self.valid_categories.remove(category.name)

        for btn in self.category_buttons:
            if btn["text"] == category.name:
                btn.config(state=tk.DISABLED)
        self.current_player.chose_category(category.name)
        self.update_scores()
        self.switch_turn()

    def switch_turn(self):
        self.current_player = (
            self.game.player1 if self.current_player == self.game.player2 else self.game.player2
        )
        if self.current_player.state.is_final():
            self.end_game()
        else:
            self.start_turn()

    def end_game(self):
        winner = self.get_winner()
        self.action_label.config(text=f"Game over! {winner} wins!")
        messagebox.showinfo("Game Over", f"{winner} wins!")

    def update_scores(self):
        self.player1_score.config(text=f"{self.game.player1.name}: {self.game.player1.get_score()}")
        self.player2_score.config(text=f"{self.game.player2.name}: {self.game.player2.get_score()}")

    def get_winner(self):
        p1_score = self.game.player1.get_score()
        p2_score = self.game.player2.get_score()
        if p1_score > p2_score:
            return self.game.player1.name
        elif p1_score < p2_score:
            return self.game.player2.name
        else:
            return "It's a tie"
