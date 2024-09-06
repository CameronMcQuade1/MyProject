import tkinter as tk


class DefaultWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Expense Tracker')
        self.root.mainloop()

DefaultWindow()
