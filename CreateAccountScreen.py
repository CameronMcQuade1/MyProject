import tkinter as tk


class CreateAccount:
    def __init__(self, parent):
        self.parent = parent
        self.account_screen = tk.Frame(parent)

        self.account_screen.pack(expand=True, fill=tk.BOTH)

    def find_all_accounts(self):
        pass

    def destroy_self(self):
        self.account_screen.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x500')
    account_frame = CreateAccount(root)
    root.mainloop()