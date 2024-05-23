import tkinter as tk
from tkinter import font
import MyMessageBoxes


class MainLogin:
    def __init__(self, parent):
        self.login_screen = tk.Frame(parent)
        self.User = tk.StringVar()
        self.Password = tk.StringVar()
        self.main_frame()
        self.login_screen.pack()


    def main_frame(self):
        self.login_frame = tk.Frame(self.login_screen, borderwidth=2, relief='groove')
        self.enter_user_label = tk.Label(self.login_frame, text='Username:')
        self.enter_username = tk.Entry(self.login_frame, textvariable=self.User)
        self.enter_password_label = tk.Label(self.login_frame, text='Password:')
        self.enter_password = tk.Entry(self.login_frame, textvariable=self.Password, show='*')
        self.show_password = tk.Button(self.login_frame, text="👁")
        self.show_password['font'] = font.Font(size=11)
        self.enter_user_label.grid(row=0, column=0)
        self.enter_username.grid(row=1, column=0)
        self.enter_password_label.grid(row=0, column=1)
        self.enter_password.grid(row=1, column=1)
        self.show_password.grid(row=1, column=2)
        self.show_password.bind('<ButtonPress-1>', lambda event: self.show_hide_password())
        self.show_password.bind('<ButtonRelease-1>', lambda event: self.show_hide_password())

        self.login_frame.pack()

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
        questions_and_answers = tk.Label(faq_frame, text=("𝗪𝗵𝗮𝘁 𝗶𝘀 𝗺𝘆 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗮𝗻𝗱 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱:"
                                                          "\n- Your Username and Password will be given to you when "
                                                          "your account is first created."
                                                          "\n𝗪𝗵𝗮𝘁 𝘁𝗼 𝗱𝗼 𝗶𝗳 𝗜'𝘃𝗲 𝗳𝗼𝗿𝗴𝗼𝘁𝘁𝗲𝗻 𝗺𝘆 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱:"
                                                          "\n- Dont worry! Just click on the 'forgot password' button "
                                                          "and answer some questions to reset it."), relief='ridge',
                                         font=8)
        questions_and_answers.grid(row=0, column=1)
        faq_frame.grid(row=0, column=1)
        quit_button = tk.Button(faq_screen, text='𝗫', background='Red', command=faq_screen.destroy, height=3)
        quit_button['font'] = font.Font(size=14)
        quit_button.grid(row=0, column=0)
        faq_screen.mainloop()

    def remove_login_frame(self):
        self.login_screen.destroy()


if __name__ == "__main__":
    test_root = tk.Tk()
    login_frame = MainLogin(test_root)
    test_root.mainloop()
