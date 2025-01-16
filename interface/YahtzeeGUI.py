import tkinter as tk
from time import sleep
from tkinter import messagebox
from game.YahtzeeGame import YahtzeeGame
from player.HumanPlayer import HumanPlayer
from state.Action import ASSIGN_ACTION_BOUNDARY
from interface.YahtzeeAssistant import YahtzeeAssistant
import os
from dotenv import load_dotenv
from database.ScoreActions import InsertScore
from database.ScoreActions import GetScore


class YahtzeeGUI:
    def __init__(self, root, categories):
        self.root = root
        self.categories = categories
        self.game = None
        self.current_player = None
        self.dice_selected = [False] * 5
        self.valid_categories = [category.name for category in categories]
        self.reroll_count = 0
        load_dotenv()
        self.assistant_response = YahtzeeAssistant(os.getenv("API_KEY"))

        self.player1_name_label = None
        self.player1_name_entry = None
        self.start_button = None

        self.bonus_p2_label = None
        self.bonus_p1_label = None
        self.score_labels = None
        self.turn_phase = None
        self.action_label = None
        self.category_buttons = None
        self.category_frame = None
        self.skip_reroll_button = None
        self.reroll_button = None
        self.roll_button = None
        self.dice_buttons = None
        self.dice_images = None
        self.dice_frame = None
        self.player2_score = None
        self.player1_score = None
        self.score_frame = None
        self.chat_display = None
        self.chat_input = None
        self.chat_bubbles_frame = None
        self.chat_messages_frame = None
        self.chat_messages_canvas = None
        self.start_button = None
        self.view_history_button = None
        self.player1_name_entry = None
        self.player1_name_label = None

        self.setup_name_entry()

    def setup_name_entry(self):
        self.root.configure(bg="#228B22")

        name_frame = tk.Frame(self.root, bg="#228B22", padx=20, pady=20)
        name_frame.pack(side=tk.TOP, pady=20)

        self.player1_name_label = tk.Label(
            name_frame,
            text="Enter your name:",
            font=("Arial", 14, "bold"),
            bg="#228B22",
            fg="white"
        )
        self.player1_name_label.pack(side=tk.LEFT, padx=10)

        self.player1_name_entry = tk.Entry(
            name_frame,
            font=("Arial", 14),
            width=15,
            relief="flat",
            highlightbackground="white",
            highlightthickness=2
        )
        self.player1_name_entry.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            command=self.start_game,
            bg="#B22222",
            fg="white",
            font=("Arial", 16, "bold"),
            relief="raised",
            bd=4
        )
        self.start_button.pack(side=tk.TOP, pady=20)
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg="#8B0000"))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg="#B22222"))

        self.view_history_button = tk.Button(
            self.root,
            text="View History",
            command=self.view_history,
            bg="#1E90FF",
            fg="white",
            font=("Arial", 16, "bold"),
            relief="raised",
            bd=4
        )
        self.view_history_button.pack(side=tk.TOP, pady=10)
        self.view_history_button.bind("<Enter>", lambda e: self.view_history_button.config(bg="#104E8B"))
        self.view_history_button.bind("<Leave>", lambda e: self.view_history_button.config(bg="#1E90FF"))

    def start_game(self):
        player1_name = self.player1_name_entry.get()
        if not player1_name.strip():
            tk.messagebox.showerror("Error", "Please enter a name before starting the game.")
            return

        loading_label = self.create_loading_label()
        loading_label.pack(side=tk.TOP, pady=20)
        self.root.update()

        if self.view_history_button:
            self.view_history_button.pack_forget()

        try:
            self.game = YahtzeeGame(player1_name, self.categories)
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while starting the game: {e}")
            loading_label.destroy()
            return

        loading_label.destroy()
        self.current_player = self.game.player1
        self.hide_name_entry_ui()
        self.setup_ui()
    
    def view_history(self):
        player1_name = self.player1_name_entry.get()
        if not player1_name.strip():
            tk.messagebox.showerror("Error", "Please enter a name to view history.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Game History")
        history_window.configure(bg="#228B22")

        history_label = tk.Label(
            history_window,
            text=f"History for {player1_name}",
            font=("Arial", 16, "bold"),
            bg="#228B22",
            fg="white"
        )
        history_label.pack(pady=10)

        history_content = tk.Text(
            history_window,
            font=("Arial", 14),
            width=50,
            height=20,
            bg="#2E8B57",
            fg="black",
            state="normal"
        )
        scores = GetScore(player1_name)
        for score in scores:
            history_content.insert(tk.END, f"• Player: {score[0]} | AI: {score[1]}\n")
        history_content.pack(pady=10, padx=10)

        back_button = tk.Button(
            history_window,
            text="Back",
            command=history_window.destroy,
            bg="#B22222",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=4
        )
        back_button.pack(pady=10)

        back_button.bind("<Enter>", lambda e: back_button.config(bg="#8B0000"))
        back_button.bind("<Leave>", lambda e: back_button.config(bg="#B22222"))

    def create_loading_label(self):
        return tk.Label(
            self.root,
            text="Loading, please wait...",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#228B22"
        )

    def hide_name_entry_ui(self):
        self.player1_name_label.pack_forget()
        self.player1_name_entry.pack_forget()
        self.start_button.pack_forget()

    def setup_ui(self):
        self.root.configure(bg="#228B22")

        main_frame = tk.Frame(self.root, bg="#228B22", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        center_panel = self.create_center_panel(main_frame)
        right_panel = self.create_right_panel(main_frame)
        chat_panel = self.create_chat_panel(main_frame)
        bottom_panel = self.create_bottom_panel()

        center_panel.grid(row=0, column=0, sticky="nsew")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        chat_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_dice_display(center_panel)
        self.create_control_buttons(center_panel)
        self.create_scoreboard(right_panel)
        self.create_scoreboard_bonus_labels(right_panel)
        self.create_category_buttons(bottom_panel)

        self.start_turn()

    def create_center_panel(self, main_frame):
        center_panel = tk.Frame(main_frame, bg="#228B22", width=350, padx=15)
        center_panel.grid(row=0, column=0, sticky="ns")
        return center_panel

    def create_right_panel(self, main_frame):
        right_panel = tk.Frame(main_frame, bg="white", relief="solid", bd=2, padx=10, pady=10)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=15)
        return right_panel

    def create_chat_panel(self, main_frame):
        chat_panel = tk.Frame(main_frame, bg="white", relief="solid", bd=2)
        chat_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        tk.Label(
            chat_panel,
            text="Chat",
            font=("Arial", 16, "bold"),
            fg="black",
            bg="white"
        ).grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        chat_display_frame = tk.Frame(chat_panel, bg="white")
        chat_display_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        chat_scrollbar = tk.Scrollbar(chat_display_frame, orient=tk.VERTICAL)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_messages_canvas = tk.Canvas(
            chat_display_frame,
            bg="white",
            yscrollcommand=chat_scrollbar.set,
            height=150,
            width=330
        )
        self.chat_messages_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scrollbar.config(command=self.chat_messages_canvas.yview)
        self.chat_bubbles_frame = tk.Frame(self.chat_messages_canvas, bg="white")
        self.chat_messages_canvas.create_window((0, 0), window=self.chat_bubbles_frame, anchor="nw")
        self.chat_messages_canvas.bind(
            "<Configure>",
            lambda e: self.chat_messages_canvas.configure(scrollregion=self.chat_messages_canvas.bbox("all"))
        )

        chat_input_frame = tk.Frame(chat_panel, bg="white", pady=5)
        chat_input_frame.grid(row=2, column=0, sticky="ew", padx=10)
        self.chat_input = tk.Entry(chat_input_frame, font=("Arial", 12), width=30)
        self.chat_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        chat_send_button = tk.Button(
            chat_input_frame,
            text="Send",
            command=self.handle_chat_input,
            bg="#6495ED",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised"
        )
        chat_send_button.grid(row=0, column=1)
        chat_panel.grid_rowconfigure(1, weight=1)

        return chat_panel

    def create_bottom_panel(self):
        bottom_panel = tk.Frame(self.root, bg="#228B22", pady=10)
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)
        return bottom_panel

    def create_dice_display(self, center_panel):
        self.dice_frame = tk.Frame(center_panel, bg="#228B22", pady=10)
        self.dice_frame.pack()

        self.dice_images = {i: tk.PhotoImage(file=f"dice_images/dice_{i}.png") for i in range(1, 7)}
        self.dice_buttons = []

        for i in range(5):
            btn = self.create_dice_button(i)
            self.dice_buttons.append(btn)

    def create_dice_button(self, i):
        btn = tk.Button(
            self.dice_frame,
            image=self.dice_images[1],
            text=f"Dice {i + 1}",
            compound="top",
            width=80,
            height=80,
            bg="white",
            state=tk.DISABLED,
            command=lambda idx=i: self.toggle_dice_selection(idx)
        )
        btn.pack(side=tk.LEFT, padx=10)
        return btn

    def create_control_buttons(self, center_panel):
        button_width = 20
        self.roll_button = self.create_button(center_panel, "Roll Dice", self.handle_turn, "#FF4500", button_width)
        self.reroll_button = self.create_button(center_panel, "Reroll Selected Dice", self.reroll_dice, "#FFD700", button_width, state=tk.DISABLED)
        self.skip_reroll_button = self.create_button(center_panel, "Keep Dice and Choose Category", self.skip_reroll, "#6495ED", button_width, state=tk.DISABLED)

        self.action_label = tk.Label(center_panel, text="", font=("Arial", 12), fg="white", bg="#228B22")
        self.action_label.pack(pady=5)

    def create_button(self, parent, text, command, bg_color, width, state=tk.NORMAL):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            width=width,
            state=state
        )
        button.pack(pady=5, fill=tk.X)
        return button

    def create_scoreboard(self, right_panel):
        tk.Label(
            right_panel,
            text="Scoreboard",
            font=("Arial", 16, "bold"),
            fg="black",
            bg="white"
        ).grid(row=0, column=0, columnspan=3, pady=5)

        self.create_scoreboard_headers(right_panel)
        self.create_scoreboard_labels(right_panel)

    def create_scoreboard_headers(self, right_panel):
        tk.Label(
            right_panel,
            text="Category",
            font=("Arial", 14, "bold"),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        ).grid(row=1, column=0, sticky="nsew", padx=3, pady=3)

        tk.Label(
            right_panel,
            text=self.game.player1.name,
            font=("Arial", 14, "bold"),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        ).grid(row=1, column=1, sticky="nsew", padx=3, pady=3)

        tk.Label(
            right_panel,
            text=self.game.player2.name,
            font=("Arial", 14, "bold"),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        ).grid(row=1, column=2, sticky="nsew", padx=3, pady=3)

    def create_scoreboard_labels(self, right_panel):
        self.score_labels = {}
        for idx, category in enumerate(self.categories, start=2):
            self.create_category_score_labels(right_panel, idx, category)

    def create_category_score_labels(self, right_panel, idx, category):
        tk.Label(
            right_panel,
            text=category.name,
            font=("Arial", 12),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        ).grid(row=idx, column=0, sticky="nsew", padx=3, pady=3)

        p1_label = tk.Label(
            right_panel,
            text="0",
            font=("Arial", 12),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        )
        p1_label.grid(row=idx, column=1, sticky="nsew", padx=3, pady=3)

        p2_label = tk.Label(
            right_panel,
            text="0",
            font=("Arial", 12),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        )
        p2_label.grid(row=idx, column=2, sticky="nsew", padx=3, pady=3)

        self.score_labels[category.name] = (p1_label, p2_label)

    def create_scoreboard_bonus_labels(self, right_panel):
        bonus_row = len(self.categories) + 2
        tk.Label(
            right_panel,
            text="Bonus",
            font=("Arial", 12, "bold"),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        ).grid(row=bonus_row, column=0, sticky="nsew", padx=3, pady=3)

        self.bonus_p1_label = tk.Label(
            right_panel,
            text="0",
            font=("Arial", 12),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        )
        self.bonus_p1_label.grid(row=bonus_row, column=1, sticky="nsew", padx=3, pady=3)

        self.bonus_p2_label = tk.Label(
            right_panel,
            text="0",
            font=("Arial", 12),
            fg="black",
            bg="white",
            relief="solid",
            bd=1
        )
        self.bonus_p2_label.grid(row=bonus_row, column=2, sticky="nsew", padx=3, pady=3)

    def create_category_buttons(self, bottom_panel):
        tk.Label(
            bottom_panel,
            text="Choose a Category",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#228B22"
        ).pack(side=tk.TOP, pady=5)

        category_frame = tk.Frame(bottom_panel, bg="#228B22")
        category_frame.pack(pady=5)

        self.category_buttons = [
            self.create_category_button(category, category_frame)
            for category in self.game.categories
        ]

        for idx, btn in enumerate(self.category_buttons):
            row = idx // 6
            col = idx % 6
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

    def create_category_button(self, category, category_frame):
        return tk.Button(
            category_frame,
            text=category.name,
            command=lambda c=category: self.choose_category(c),
            state=tk.DISABLED,
            bg="#FF6347",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            width=15
        )

    def handle_chat_input(self):
        player_message = self.chat_input.get().strip()
        if not player_message:
            return

        response = self.assistant_response.generate_chat_response(player_message)
        self.add_message(player_message, "user")
        self.add_message(response, "system")
        self.chat_input.delete(0, tk.END)

    def add_message(self, message, sender):
        bg_color = "#6495ED" if sender == "user" else "white"
        message_frame = tk.Frame(self.chat_bubbles_frame, bg="white", pady=5)
        message_frame.pack(anchor="e" if sender == "user" else "w",
                           fill="x",
                           padx=5)
        tk.Label(
            message_frame,
            text=message,
            wraplength=300,
            bg=bg_color,
            font=("Arial", 12),
            padx=10,
            pady=5,
            anchor="w",
            justify="left"
        ).pack(anchor="e" if sender == "user" else "w",
               padx=10,
               pady=2)

        self.chat_messages_canvas.update_idletasks()
        self.chat_messages_canvas.configure(scrollregion=self.chat_messages_canvas.bbox("all"))
        self.chat_messages_canvas.yview_moveto(1)

    def enable_category_selection(self):
        for btn in self.category_buttons:
            if btn["text"] in self.valid_categories:
                btn.config(state=tk.NORMAL, bg="#32CD32")

    def disable_category_selection(self):
        for btn in self.category_buttons:
            btn.config(state=tk.DISABLED, bg="#FF6347")

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
        for idx, btn in enumerate(self.dice_buttons):
            if not self.dice_selected[idx]:
                btn.config(state=tk.NORMAL, bg="white")
            else:
                btn.config(state=tk.NORMAL, bg="red")

    def get_selected_dice_indices(self):
        return [idx for idx, selected in enumerate(self.dice_selected) if selected]

    def update_dice_display(self):
        for i, val in enumerate(self.current_player.state.dice):
            self.dice_buttons[i].config(image=self.dice_images[val])

    def update_scores(self):
        for category in self.categories:
            p1_score = self.game.player1.state.scores[category]
            p2_score = self.game.player2.state.scores[category]

            self.score_labels[category.name][0].config(text=p1_score)
            self.score_labels[category.name][1].config(text=p2_score)

            if self.game.player1.state.scores[category] is not None:
                self.score_labels[category.name][0].config(bg="#98FB98")
            else:
                self.score_labels[category.name][0].config(bg="white")

            if self.game.player2.state.scores[category] is not None:
                self.score_labels[category.name][1].config(bg="#98FB98")
            else:
                self.score_labels[category.name][1].config(bg="white")

        p1_bonus = self.game.player1.get_bonus()
        p2_bonus = self.game.player2.get_bonus()
        self.bonus_p1_label.config(text=p1_bonus)
        self.bonus_p2_label.config(text=p2_bonus)

        if p1_bonus != 0:
            self.bonus_p1_label.config(bg="#98FB98")
        else:
            self.bonus_p1_label.config(bg="white")

        if p2_bonus != 0:
            self.bonus_p2_label.config(bg="#98FB98")
        else:
            self.bonus_p2_label.config(bg="white")

    def toggle_dice_selection(self, idx):
        self.dice_selected[idx] = not self.dice_selected[idx]
        btn = self.dice_buttons[idx]
        if self.dice_selected[idx]:
            btn.config(bg="red")
        else:
            btn.config(bg="white")

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

    def choose_category(self, category):
        if category.name in self.valid_categories:
            self.valid_categories.remove(category.name)

        for btn in self.category_buttons:
            if btn["text"] == category.name:
                btn.config(state=tk.DISABLED)
        self.current_player.chose_category(category.name)
        self.update_scores()
        self.switch_turn()

    def execute_ai_decision(self):
        self.current_player.action = self.current_player.strategy.choose_action(self.current_player.state)
        while self.current_player.get_rerolls() is not None:
            sleep(2)
            self.current_player.handle_rerolls()
            self.update_dice_display()

        self.turn_phase = "choose_category"
        self.action_label.config(text=f"{self.current_player.name} is choosing a category.")
        self.current_player.chose_category()
        self.update_scores()
        sleep(2)
        self.switch_turn()

    def get_winner(self):
        p1_score = self.game.player1.get_score()
        p2_score = self.game.player2.get_score()
        if p1_score > p2_score:
            return self.game.player1.name
        elif p1_score < p2_score:
            return self.game.player2.name
        else:
            return "It's a tie"

    def start_turn(self):
        self.turn_phase = "roll"
        self.reroll_count = 0
        self.dice_selected = [False] * 5
        for btn in self.dice_buttons:
            btn.config(bg="white")
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
            self.action_label.config(
                text=f"{self.current_player.name}'s turn! Deciding to reroll or choose a category.")
            self.roll_button.config(state=tk.DISABLED)

            if isinstance(self.current_player, HumanPlayer):
                self.enable_reroll_options()
            else:
                self.execute_ai_decision()

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
        p1_score = self.game.player1.get_score()
        p2_score = self.game.player2.get_score()
        InsertScore(p1_score, p2_score, self.game.player1.name)
        if winner == "It's a tie":
            self.action_label.config(text="Game over! It's a tie!")
            messagebox.showinfo(
                "Game Over",
                f"It's a tie!\n\nFinal Scores:\nPlayer 1: {p1_score}\nPlayer 2: {p2_score}"
            )
        else:
            self.action_label.config(text=f"Game over! {winner} wins!")
            messagebox.showinfo(
                "Game Over",
                f"{winner} wins!\n\nFinal Scores:\nPlayer 1: {p1_score}\nPlayer 2: {p2_score}"
            )
