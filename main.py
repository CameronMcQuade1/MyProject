import MyAccountsDatabase
import MyMessageBoxes
import LoginScreen
import tkinter as tk


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Expense Tracker')
        self.menu_bar()
        self.show_login_screen()
        self.centre_window(self.root, 1400, 700)
        self.root.mainloop()

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
        settings_menu = tk.Menu(main_bar)
        settings_menu.add_command(label='Change Background Colour')
        main_bar.add_cascade(label='Settings', menu=settings_menu)
        help_menu = tk.Menu(main_bar)
        help_menu.add_command(label='Login Help')
        help_menu.add_command(label='Frequently Asked Questions',
                              command=LoginScreen.MainLogin.frequently_asked_questions_gui)
        main_bar.add_cascade(label='Help', menu=help_menu)

    def show_login_screen(self):
        login_screen = LoginScreen.MainLogin(self.root)


MainGUI()
