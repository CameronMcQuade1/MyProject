import customtkinter as ctk
from PIL import Image
import MyMessageBoxes
from MyCustomFunctions import *

class MainLogin:
    def __init__(self, parent):
        self.parent = parent

        # Set appearance mode and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Creating a customtkinter frame for the login screen
        self.login_screen = ctk.CTkFrame(parent, fg_color="white")
        self.User = ctk.StringVar()
        self.Password = ctk.StringVar()
        self.main_frame()
        self.login_screen.pack(fill=ctk.BOTH, expand=True)

    def main_frame(self):
        # Main login frame with larger dimensions
        self.login_frame = ctk.CTkFrame(self.login_screen, width=400, height=300, corner_radius=15)
        self.login_frame.place(anchor='center', relx=0.5, rely=0.5)

        # Title Label
        title_label = ctk.CTkLabel(self.login_frame, text="£xpense Tracker", font=("Helvetica", 24, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor='center')

        # Entry boxes and placeholder text
        self.enter_username = ctk.CTkEntry(self.login_frame, textvariable=self.User, placeholder_text='Username',
                                           width=250, height=30)
        self.enter_password = ctk.CTkEntry(self.login_frame, textvariable=self.Password, placeholder_text='Password',
                                           show='', width=250, height=30)

        # Login and Forgot Password buttons
        self.login_button = ctk.CTkButton(self.login_frame, command=self.try_login, text="Login", height=40, width=120,
                                          corner_radius=20)
        self.forgot_pass = ctk.CTkButton(self.login_frame, command=self.new_password, text="Forgot Password?",
                                         height=30, width=150, corner_radius=20, fg_color="transparent",
                                         text_color=("gray20", "gray80"))

        # View password button
        ShowHidePasswordWidget(self.login_frame, self.enter_password, 0.87, 0.5)


        # Placing widgets with padding for better spacing
        self.enter_username.place(relx=0.5, rely=0.3, anchor='center')
        self.enter_password.place(relx=0.5, rely=0.5, anchor='center')
        self.login_button.place(relx=0.5, rely=0.7, anchor='center')
        self.forgot_pass.place(relx=0.5, rely=0.85, anchor='center')

        # Event binding for custom placeholder text and show/hide password functionality
        EntryPlaceHolderText(self.login_screen, self.enter_username, 'Username')
        EntryPlaceHolderText(self.login_screen, self.enter_password, 'Password')

    def try_login(self):
        # Implementation for login attempt
        pass

    def new_password(self):
        # Implementation for new password functionality
        pass

    def remove_login_frame(self):
        self.login_screen.destroy()

if __name__ == "__main__":
    test_root = ctk.CTk()
    test_root.geometry("1400x700")
    test_root.title("Login Screen")
    # Adding a gradient background color
    test_root.configure(bg="light blue")
    starting_frame = MainLogin(test_root)
    test_root.mainloop()
