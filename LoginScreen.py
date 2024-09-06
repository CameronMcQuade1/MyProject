import tkinter as tk
from tkinter import font
import MyMessageBoxes
from MyCustomFunctions import EntryPlaceHolderText, ShowHidePassword


class MainLogin:
    def __init__(self, parent):
        self.parent = parent
        self.login_screen = tk.Frame(parent)
        self.User = tk.StringVar()
        self.Password = tk.StringVar()
        self.main_frame()
        self.login_screen.pack(fill=tk.BOTH, expand=True)

    def main_frame(self):
        # Main login frame with larger dimensions
        self.login_frame = tk.Frame(self.login_screen, borderwidth=2, relief='groove', width=375, height=215)
        self.login_frame.place(anchor='center', relx=0.5, rely=0.35)

        # Entry boxes and placeholder text
        self.enter_username = tk.Entry(self.login_frame, textvariable=self.User, fg='grey', width=40)
        self.enter_password = tk.Entry(self.login_frame, textvariable=self.Password, fg='grey', show='', width=40)
        self.login_button = tk.Button(self.login_frame, command=self.try_login, text="Login", height=2, width=20)
        self.forgot_pass = tk.Button(self.login_frame, command=self.new_password, text="Forgot Password",
                                     height=2, width=20)

        # View password
        self.show_password = tk.Button(self.login_frame, text="👁", width=2, height=1)
        self.show_password['font'] = font.Font(size=11)

        # Placing widgets with padding for better spacing
        self.enter_username.place(relx=0.5, rely=0.2, anchor='center')
        self.enter_password.place(relx=0.5, rely=0.4, anchor='center')
        self.show_password.place(relx=0.9, rely=0.4, anchor='center')
        self.login_button.place(relx=0.5, rely=0.6, anchor='center')
        self.forgot_pass.place(relx=0.5, rely=0.85, anchor='center')

        # Event binding
        EntryPlaceHolderText(self.login_screen, self.enter_username, 'Username')
        EntryPlaceHolderText(self.login_screen, self.enter_password, 'Password')
        self.enter_password.bind('<ButtonPress-1>', lambda event: self.enter_password.config(show='*'))
        self.show_password.bind('<ButtonPress-1>', lambda event: ShowHidePassword(self.enter_password))
        self.show_password.bind('<ButtonRelease-1>', lambda event: ShowHidePassword(self.enter_password))

    def try_login(self):
        pass

    def new_password(self):
        pass

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
        faq_frame.pack(expand=True, fill=tk.BOTH)
        faq_screen.mainloop()

    def remove_login_frame(self):
        self.login_screen.destroy()


if __name__ == "__main__":
    test_root = tk.Tk()
    starting_frame = MainLogin(test_root)
    test_root.geometry("1400x700")
    test_root.mainloop()
