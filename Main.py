import MyDatabase
import MyMessageBoxes
import LoginScreen
import CreateAccountScreen
import customtkinter as ctk
import tkinter as tk


class MainApp:
    def __init__(self):
        # Initialize the custom tkinter window
        ctk.set_appearance_mode("light")  # Optional: Set to 'light' or 'dark'
        ctk.set_default_color_theme("blue")  # Optional: Set color theme
        self.root = ctk.CTk()  # Use CTk instead of Tk
        self.root.title('Expense Tracker')
        self.centre_window(self.root, 850, 525)
        self.run_sequence()  # Start the login sequence
        self.root.mainloop()  # Start the main loop

    def run_sequence(self):
        if MyDatabase.AccountsDatabase().return_account_amount() == 0:
            msg = MyMessageBoxes.ShowMessage.show_warning("No accounts detected.\n You will need to make an account.")
            if msg == "Cancel":
                exit()
            elif msg == "Okay":
                self.root.geometry("325x175+750+250")
                CreateAccountScreen.CreateAccount(self.root)
            else:
                MyMessageBoxes.ShowMessage.show_info("No previous accounts have been detected. You will now need to "
                                                     "make one.")
                self.root.geometry("325x175+750+250")
                CreateAccountScreen.CreateAccount(self.root)
        else:
            LoginScreen.MainLogin(self.root)

    @staticmethod
    def centre_window(target, width, height):
        screen_width = target.winfo_screenwidth()
        screen_height = target.winfo_screenheight()
        centre_x = (screen_height / 2) - (width / 2)
        centre_y = (screen_height / 2) - (height / 2)
        target.geometry('%dx%d+%d+%d' % (width, height, centre_x, centre_y))
        target.resizable(False, False)


def app():
    MainApp()


if __name__ == '__main__':
    app()  # Call the app function to run the application
