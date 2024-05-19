import tkinter as tk
from tkinter import ttk, font
import MyMessageBoxes


class MainLogin:
    def __init__(self):
        self.login_screen = tk.Tk()
        self.User = tk.StringVar()
        self.Password = tk.StringVar()
        self.login_screen.title("Expense Tracker")
        self.centre_window(self.login_screen, 1400, 700)
        self.main_frame()
        self.menu_bar()
        self.login_screen.mainloop()

    @staticmethod
    def centre_window(target, width, height):
        screen_width = target.winfo_screenwidth()
        screen_height = target.winfo_screenheight()
        centre_x = (screen_width / 2) - (width / 2)
        centre_y = (screen_height / 2) - (height / 2)
        target.geometry('%dx%d+%d+%d' % (width, height, centre_x, centre_y))

    def main_frame(self):
        login_frame = ttk.Frame(self.login_screen, borderwidth=2, relief='groove')
        enter_user_label = ttk.Label(login_frame, text='Username:')
        enter_username = ttk.Entry(login_frame, textvariable=self.User)
        enter_password_label = ttk.Label(login_frame, text='Password:')
        enter_password = ttk.Entry(login_frame, textvariable=self.Password, show='*')
        show_password = ttk.Button(login_frame, text='Show')
        enter_user_label.grid(row=0, column=0)
        enter_username.grid(row=1, column=0)
        enter_password_label.grid(row=0, column=1)
        enter_password.grid(row=1, column=1)
        show_password.grid(row=1, column=2)

        login_frame.pack()

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
        faq_screen = tk.Toplevel()
        faq_screen.title("FAQ:")
        self.centre_window(faq_screen, 650, 125)
        self.exit_button(faq_screen)
        faq_frame = ttk.Frame(faq_screen)
        questions_and_answers = ttk.Label(faq_frame, text=("𝗪𝗵𝗮𝘁 𝗶𝘀 𝗺𝘆 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱:"
                                                           "\n- Your Username and Password will be given to you when "
                                                           "your account is first created."
                                                           "\n𝗪𝗵𝗮𝘁 𝘁𝗼 𝗱𝗼 𝗶𝗳 𝗜'𝘃𝗲 𝗳𝗼𝗿𝗴𝗼𝘁𝘁𝗲𝗻 𝗺𝘆 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱:"
                                                           "\n- Dont worry! Just click on the 'forgot password' button "
                                                           "and answer some questions to reset it."), relief='ridge',
                                          font=20)
        questions_and_answers.pack()
        faq_frame.grid(row=1, column=0)
        faq_screen.mainloop()


    def exit_button(self, parent):
        quit_button = tk.Button(parent, text='𝗫', background='Red', command=parent.destroy)
        font_size = font.Font(size=14)
        quit_button['font'] = font_size
        quit_button.grid(row=0, column=0, sticky='w')


MainLogin()
