from interface.YahtzeeGUI import YahtzeeGUI
from state.Category import categories
import tkinter as tk


def main():
    root = tk.Tk()
    YahtzeeGUI(root, categories)
    root.mainloop()


if __name__ == '__main__':
    main()
