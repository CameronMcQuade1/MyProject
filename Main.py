import MyAccountsDatabase
import MyMessageBoxes
import LoginScreen
import tkinter as tk


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Expense Tracker')
        self.menu_bar()
        self.run_sequence()
        self.centre_window(self.root, 600, 370)
        self.root.mainloop()

    def run_sequence(self):
        LoginScreen.StarterUI(self.root)

    @staticmethod
    def centre_window(target, width, height):
        screen_width = target.winfo_screenwidth()
        screen_height = target.winfo_screenheight()
        centre_x = (screen_width / 2) - (width / 2)
        centre_y = (screen_height / 2) - (height / 2)
        target.geometry('%dx%d+%d+%d' % (width, height, centre_x, centre_y))

    def menu_bar(self):
        main_bar = tk.Menu()
        self.root.config(menu=main_bar)
        settings_menu = tk.Menu(main_bar, tearoff=False)
        settings_menu.add_command(label='Change Background Colour')
        main_bar.add_cascade(label='Settings', menu=settings_menu)
        help_menu = tk.Menu(main_bar, tearoff=False)
        help_menu.add_command(label='Frequently Asked Questions',
                              command=LoginScreen.MainLogin.frequently_asked_questions_gui)
        main_bar.add_cascade(label='Help', menu=help_menu)


def app():
    main_db = MyAccountsDatabase.AccountsDatabase()
    main_db.create_root_account()
    print(main_db.check_accounts_amount())
    MainApp()


if __name__ == '__main__':
    app()
