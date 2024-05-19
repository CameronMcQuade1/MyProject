import tkinter as tk
from tkinter import ttk
import MyMessageBoxes


class MainLogin:
    def __init__(self):
        self.login_screen = tk.Tk()
        self.main_frame()
        self.menu_bar()
        self.login_screen.mainloop()

    def main_frame(self):
        login_frame = ttk.Frame(self.login_screen, borderwidth=2, relief='groove', cursor='arrow')
        enter_user_label = ttk.Label(login_frame, text='Username:')
        enter_user_label.pack()
        login_frame.place(relx=0.5, rely=0.5)

    def menu_bar(self):
        main_bar = tk.Menu()
        self.login_screen.config(menu=main_bar)
        settings_menu = tk.Menu(main_bar)
        settings_menu.add_command(label='Change Background Colour')
        main_bar.add_cascade(label='Settings', menu=settings_menu)
        help_menu = tk.Menu(main_bar)
        help_menu.add_command(label='Login Help')
        help_menu.add_command(label='Frequently Asked Questions', command=self.frequently_asked_questions_gui)
        main_bar.add_cascade(label='Help', menu=help_menu)

    def frequently_asked_questions_gui(self):
        MyMessageBoxes.ShowMessage.show_info("Whats My Username and Password:"
                                             "\n- Your Username and Password will be given to you when "
                                             "your account is first created."
                                             "\nWhat to do if I've forgotten my password:"
                                             "\n- Dont worry! Just click on the 'forgot password' button "
                                             "and answer some questions to reset it.")



MainLogin()
