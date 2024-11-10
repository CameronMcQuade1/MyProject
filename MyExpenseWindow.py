import customtkinter as ctk
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import MyMessageBoxes
import MyCustomFunctions
import MyDatabase


class DefaultWindow:
    def __init__(self, parent, current_user):
        self.parent = parent
        self.current_user = current_user

        self.root = ctk.CTkFrame(parent)
        self.root.pack(expand=True, fill="both")

        self.nb = ctk.CTkTabview(self.root, width=500, height=400)
        self.nb.pack(expand=True, fill="both")

        self.setup_notebook()

    def setup_notebook(self):
        self.nb.add("Tracker Settings")
        self.nb.add("Expenses")
        self.nb.add("Graphs")
        self.nb.add("Tables")
        self.nb.add("Plotter")
        self.nb.set("Expenses")

        self.setup_expense_window()

    def setup_expense_window(self):
        self.create_tracker_settings_tab()
        self.create_expenses_tab()
        self.create_graphs_tab()

    def remove_main_window(self):
        self.parent.withdraw()

    def show_main_window(self, target):
        target.withdraw()
        self.parent.deiconify()

    def create_tracker_settings_tab(self):
        pass

    def create_expenses_tab(self):
        # Access the "Expenses" tab directly
        expenses_tab = self.nb.tab("Expenses")

        #  Initialising the icons for widgets
        green_plus_image_path = "GreenPlusImage.png"
        green_plus_image = Image.open(green_plus_image_path)
        green_plus_image = green_plus_image.resize((60, 60))  # Resize to fit button
        green_plus_image = ctk.CTkImage(light_image=green_plus_image, size=(60, 60))

        red_remove_image_path = "RedRemoveImage.png"
        red_remove_image = Image.open(red_remove_image_path)
        red_remove_image = red_remove_image.resize((60, 60))  # Resize to fit button
        red_remove_image = ctk.CTkImage(light_image=red_remove_image, size=(60, 60))

        download_file_image_path = "DownloadFileImage.png"
        download_file_image = Image.open(download_file_image_path)
        download_file_image = download_file_image.resize((60, 60))  # Resize to fit button
        download_file_image = ctk.CTkImage(light_image=download_file_image, size=(60, 60))

        spreadsheet_image_path = "SpreadsheetImage.png"
        spreadsheet_image = Image.open(spreadsheet_image_path)
        spreadsheet_image = spreadsheet_image.resize((60, 60))  # Resize to fit button
        spreadsheet_image = ctk.CTkImage(light_image=spreadsheet_image, size=(60, 60))

        # Label for total expenses from current user
        total_expenses_from_user = MyDatabase.AccountsDatabase().return_total_inputted_from_user(self.current_user)
        total_expenses_summed = MyDatabase.AccountsDatabase().return_expenses_summed(self.current_user)
        self.expense_view_label = ctk.CTkLabel(expenses_tab, text=f"Total Expenses From User '{self.current_user}':\n"
                                                                  f"{total_expenses_from_user} Expenses, Totalling £"
                                                                  f"{total_expenses_summed}.",
                                                                  font=("Arial", 18))
        self.expense_view_label.place(x=300, y=20)  # Adjust coordinates as needed

        # Add Expense button
        self.add_expenses_button = ctk.CTkButton(expenses_tab, image=green_plus_image, command=self.add_expense,
                                                 width=200, height=100, text="Add Expense", compound="bottom",
                                                 font=("Arial", 16))
        self.add_expenses_button.place(x=175, y=100)

        # View Expenses button
        self.remove_expenses_button = ctk.CTkButton(expenses_tab, image=red_remove_image, command=self.remove_expense,
                                                    width=200, height=100, text="Remove Expense", compound="bottom",
                                                    font=("Arial", 16))
        self.remove_expenses_button.place(x=450, y=100)

        # Remove Expense button
        self.view_expenses_button = ctk.CTkButton(expenses_tab, image=spreadsheet_image, command=self.view_expenses,
                                                  width=200, height=100, text="View Expenses", compound="bottom",
                                                  font=("Arial", 16))
        self.view_expenses_button.place(x=175, y=250)

        self.export_expenses_button = ctk.CTkButton(expenses_tab, image=download_file_image,
                                                    command=self.export_expenses, width=200, height=100,
                                                    text="Export Expenses", compound="bottom", font=("Arial", 16))
        self.export_expenses_button.place(x=450, y=250)

    def add_expense(self):
        # Create a new CTk window
        self.remove_main_window()
        self.add_expense_window = ctk.CTk()  # Or ctk.CTkToplevel(self.parent) to make it a child of the main window
        self.add_expense_frame = ctk.CTkFrame(self.add_expense_window)
        self.add_expense_frame.pack(expand=True, fill="both")
        self.add_expense_window.title("Add Expense")
        self.add_expense_window.geometry("400x300+700+200")  # Customize the size

        # Customize this window as needed
        label = ctk.CTkLabel(self.add_expense_frame, text="Add Expense:", font=("Arial", 18))
        label.pack(pady=20)

        name_label = ctk.CTkLabel(self.add_expense_frame, text="Name of item:")
        name_label.place(x=50, y=60)
        name_entry = ctk.CTkEntry(self.add_expense_frame)
        name_entry.place(x=200, y=60)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, name_entry, "Name")

        quantity_label = ctk.CTkLabel(self.add_expense_frame, text="Quantity purchased:")
        quantity_label.place(x=50, y=95)
        quantity_entry = ctk.CTkEntry(self.add_expense_frame)
        quantity_entry.place(x=200, y=95)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, quantity_entry, "Quantity")

        price_label = ctk.CTkLabel(self.add_expense_frame, text="Price per unit:")
        price_label.place(x=50, y=130)
        price_entry = ctk.CTkEntry(self.add_expense_frame)
        price_entry.place(x=200, y=130)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, price_entry, "Price")

        type_label = ctk.CTkLabel(self.add_expense_frame, text="Item type:")
        type_label.place(x=50, y=165)
        type_options = ["Rent", "Utilities", "Salaries", "Insurance", "Equipment", "Supplies", "Marketing", "Services",
                        "Training", "Travel", "Food", "Other"]
        type_option_menu = ctk.CTkOptionMenu(self.add_expense_frame, values=type_options)
        type_option_menu.set("Type:")
        type_option_menu.place(x=200, y=165)

        user_label = ctk.CTkLabel(self.add_expense_frame, text="User:")
        user_label.place(x=50, y=200)
        user_entry = ctk.CTkEntry(self.add_expense_frame)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, user_entry, self.current_user)
        user_entry.configure(state="disabled")
        user_entry.place(x=200, y=200)

        back_button = ctk.CTkButton(self.add_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.add_expense_window), width=140)
        back_button.place(x=50, y=240)
        submit_button = ctk.CTkButton(self.add_expense_frame, text="Submit",
                                      width=140, command=self.submit_expense_db)
        submit_button.place(x=200, y=240)

        self.add_expense_window.mainloop()

    def submit_expense_db(self):
        pass

    def remove_expense(self):
        # Create a new CTk window
        self.remove_main_window()
        self.remove_expense_window = ctk.CTk()  # Or ctk.CTkToplevel(self.parent) to make it a child of the main window
        self.remove_expense_frame = ctk.CTkFrame(self.remove_expense_window)
        self.remove_expense_frame.pack(expand=True, fill="both")
        self.remove_expense_window.title("Remove Expense")
        self.remove_expense_window.geometry("400x300+700+200")  # Customize the size
        self.expense_spreadsheet = MyDatabase.ExpenseViewer(self.current_user, self.remove_expense_frame)
        back_button = ctk.CTkButton(self.remove_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.remove_expense_window), width=140)
        back_button.place(x=15, y=250)
        self.remove_expense_window.mainloop()

    def view_expenses(self):
        self.remove_main_window()
        self.view_expense_window = ctk.CTk()
        self.view_expense_frame = ctk.CTkFrame(self.view_expense_window)
        self.view_expense_frame.pack(expand=True, fill="both")
        self.view_expense_window.title("View Expenses")
        self.view_expense_window.geometry("400x300+700+200")
        self.excel_expense_spreadsheet = MyDatabase.ExpenseExcelSpreadsheet(self.current_user, self.view_expense_frame)
        back_button = ctk.CTkButton(self.view_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.view_expense_window), width=140)
        back_button.place(x=15, y=250)
        self.view_expense_window.mainloop()

    def export_expenses(self):
        self.remove_main_window()
        download_table = MyMessageBoxes.ShowMessage.ask_question("Are you sure you want to download? "
                                                                 "Go to 'View Expenses' to see what you will"
                                                                 " be downloading.",
                                                                 "No", "Yes", "Back")
        if download_table == "Yes":
            try:
                MyDatabase.ExpenseExcelSpreadsheet(self.current_user, ctk.CTk()).download_expenses()
                MyMessageBoxes.ShowMessage.show_info("Spreadsheet downloaded successfully.")
            except Exception as error:
                MyMessageBoxes.ShowMessage.show_info(f"Something went wrong: {str(error)}")
        self.show_main_window(ctk.CTk())

    def create_income_tab(self):
        pass

    def create_graphs_tab(self):
        graphs_tab = self.nb.tab("Graphs")

        # Fetch user expenses over time
        expenses = MyDatabase.AccountsDatabase().return_expenses_from_user(
            self.current_user)  # Assuming self.db is an instance of AccountsDatabase

        # Extract dates and expense amounts for plotting
        dates = [expense['Date'] for expense in expenses]
        total_amounts = [expense['Price'] * expense['Quantity'] for expense in expenses]

        # Set up the matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor('#cfcfcf')
        ax = fig.add_subplot(111)
        ax.plot(dates, total_amounts, marker='o', linestyle='-', color='b')

        # Configure the graph
        ax.set_title(f"Expenses For User: {self.current_user}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Expense")
        fig.autofmt_xdate()  # Rotate date labels for better readability

        # Embed the graph in the tkinter interface
        canvas = FigureCanvasTkAgg(fig, master=graphs_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_plotter_tab(self):
        pass


class AdminWindow(DefaultWindow):
    def __init__(self, parent, current_user):
        super().__init__(parent, current_user)
        self.nb.add("Income")
        self.nb.add("Accounts")


if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Expense Tracker")
    root.geometry('850x525+425+175')
    root.resizable(False, False)

    account_frame = DefaultWindow(root, "test")
    root.mainloop()
