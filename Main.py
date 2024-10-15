import MyDatabase
import MyMessageBoxes
import LoginScreen
import customtkinter as ctk
import tkinter as tk


class MainApp:
    def __init__(self):
        # Initialize the custom tkinter window
        ctk.set_appearance_mode("light")  # Optional: Set to 'light' or 'dark'
        ctk.set_default_color_theme("blue")  # Optional: Set color theme

        self.root = ctk.CTk()  # Use CTk instead of Tk
        self.root.title('Expense Tracker')
        self.menu_bar()  # Set up the menu bar
        self.run_sequence()  # Start the login sequence
        self.centre_window(self.root, 1000, 620)  # Center the window
        self.root.mainloop()  # Start the main loop

    def run_sequence(self):
        # Display the login screen
        LoginScreen.MainLogin(self.root)

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
        help_menu.add_command(label='Frequently Asked Questions')
        main_bar.add_cascade(label='Help', menu=help_menu)


def app():
    main_db = MyDatabase.AccountsDatabase()
    MainApp()


if __name__ == '__main__':
    app()  # Call the app function to run the application
