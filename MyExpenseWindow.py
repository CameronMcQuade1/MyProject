import customtkinter as ctk
import tkinter as tk


class DefaultWindow:
    def __init__(self, parent):
        self.parent = parent

        self.root = ctk.CTkFrame(parent)
        self.root.pack(expand=True, fill="both")

        self.nb = ctk.CTkTabview(self.root, width=500, height=400)
        self.nb.pack(expand=True, fill="both")

        self.setup_notebook()

    def setup_notebook(self):
        self.nb.add("Tracker Settings")
        self.nb.add("Expenses")
        self.nb.add("Income")
        self.nb.add("Graphs")
        self.nb.add("Tables")
        self.nb.add("Plotter")
        self.nb.set("Expenses")

        self.setup_expense_window()

    def setup_expense_window(self):
        pass


class AdminWindow(DefaultWindow):
    pass


if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Expense Tracker")
    root.geometry('1100x680+250+50')
    root.resizable(False, False)

    account_frame = DefaultWindow(root)
    root.mainloop()
