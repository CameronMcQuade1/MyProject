import tkinter as tk
from tkinter import font
import MyMessageBoxes


class StarterUI:
    def __init__(self, parent):
        self.parent = parent
        self.starting_frame = tk.Frame(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.show_options()
        self.starting_frame.place(anchor="center", relx=.5, rely=.2)

    def show_options(self):
        options_menu = tk.Frame(self.starting_frame)
        login_button = tk.Button(options_menu, text="LOGIN", command=self.goto_login)
        login_button.grid(row=0, column=0)
        options_menu.pack(fill=tk.BOTH, expand=True)

    def goto_login(self):
        self.starting_frame.destroy()
        MainLogin(self.parent)


class MainLogin:
    def __init__(self, parent):
        self.login_screen = tk.Frame(parent)
        self.User = tk.StringVar()
        self.Password = tk.StringVar()
        self.main_frame()
        self.login_screen.place(anchor="center", relx=.5, rely=.2)

    def main_frame(self):
        self.login_frame = tk.Frame(self.login_screen, borderwidth=2, relief='groove')
        self.enter_user_label = tk.Label(self.login_frame, text='Username:')
        self.enter_username = tk.Entry(self.login_frame, textvariable=self.User)
        self.enter_password_label = tk.Label(self.login_frame, text='Password:')
        self.enter_password = tk.Entry(self.login_frame, textvariable=self.Password, show='*')
        self.show_password = tk.Button(self.login_frame, text="👁", width=2, height=1)
        self.show_password['font'] = font.Font(size=11)
        self.enter_user_label.grid(row=0, column=0)
        self.enter_username.grid(row=1, column=0)
        self.enter_password_label.grid(row=0, column=1)
        self.enter_password.grid(row=1, column=1)
        self.show_password.grid(row=1, column=2)
        self.show_password.bind('<ButtonPress-1>', lambda event: self.show_hide_password())
        self.show_password.bind('<ButtonRelease-1>', lambda event: self.show_hide_password())

        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_hide_password(self):
        if self.enter_password.cget('show') == '':
            self.enter_password.config(show='*')
        else:
            self.enter_password.config(show='')

    @staticmethod
    def frequently_asked_questions_gui():
        faq_screen = tk.Toplevel(background='grey')
        faq_screen.title("FAQ:")
        faq_frame = tk.Frame(faq_screen)
        questions_and_answers = tk.Label(faq_frame, text=("What is my username and password:"
                                                          "\n- Your Username and Password will be given to you when "
                                                          "your account is first created."
                                                          "\nWhat to do if I've forgotten my password:"
                                                          "\n- Dont worry! Just click on the 'forgot password' button "
                                                          "and answer some questions to reset it."), relief='ridge',
                                         font=8)
        questions_and_answers.grid(row=0, column=1)
        faq_frame.grid(row=0, column=1)
        faq_screen.mainloop()

    def remove_login_frame(self):
        self.login_screen.destroy()


if __name__ == "__main__":
    test_root = tk.Tk()
    starting_frame = StarterUI(test_root)
    test_root.geometry("1400x700")
    test_root.mainloop()
