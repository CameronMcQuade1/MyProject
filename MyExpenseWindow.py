import customtkinter as ctk
from PIL import Image
import seaborn as sns
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import CreateAccountScreen
import MyMessageBoxes
import MyCustomFunctions
import MyDatabase
import LoginScreen
from collections import defaultdict
from datetime import datetime, timedelta, date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests
from decimal import Decimal
import subprocess

import PasswordHasher


class DefaultWindow:
    def __init__(self, parent, current_user):
        self.parent = parent
        self.current_user = current_user
        self.main_db = MyDatabase.AccountsDatabase()
        self.root = ctk.CTkFrame(parent)
        self.root.pack(expand=True, fill="both")
        self.menu_bar()

        self.nb = ctk.CTkTabview(self.root, width=500, height=400)
        self.nb.pack(expand=True, fill="both")

        self.setup_notebook()

    def setup_notebook(self):
        self.nb.add("Expenses")
        self.nb.add("Graphs")
        self.nb.add("Table")
        self.nb.add("Predictor")

        self.setup_expense_window()

    def setup_expense_window(self):
        self.create_expenses_tab()
        self.create_graphs_tab()
        self.create_table_tab()
        self.create_predictor_tab()

    def remove_main_window(self):
        self.parent.withdraw()

    def show_main_window(self, target=None):
        target.withdraw() if target else None
        self.expense_view_label.destroy()
        self.create_expense_label(self.nb.tab("Expenses"), 300, 20)
        self.parent.deiconify()

    def set_current_tab(self, nb_tab):
        self.nb.set(nb_tab)

    def menu_bar(self):
        main_bar = tk.Menu()
        self.parent.configure(menu=main_bar)

        # Settings Menu
        settings_menu = tk.Menu(main_bar, tearoff=False)
        main_bar.add_cascade(label='Settings', menu=settings_menu)

        # Submenu for changing background color
        self.bg_colour_menu = tk.Menu(settings_menu, tearoff=False)
        settings_menu.add_cascade(label='Change Background Colour', menu=self.bg_colour_menu)

        # Options for background color modes
        self.color_modes = ["Light", "Dark"]
        self.current_colour_mode = tk.StringVar(value="Light")  # Default selection
        for mode in self.color_modes:
            self.bg_colour_menu.add_radiobutton(
                label=mode,
                variable=self.current_colour_mode,
                command=lambda: self.change_background_colour(self.current_colour_mode.get(), main_bar)
            )

        # Help Menu
        help_menu = tk.Menu(main_bar, tearoff=False)
        main_bar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Logging in', command=lambda:
                              MyMessageBoxes.ShowMessage().show_info("Use the Username given to you in your email "
                                                                     "and your password to log in.\nIf there are no "
                                                                     "accounts in the database, you have to make "
                                                                     "one for yourself."))
        help_menu.add_command(label='Using the app', command=lambda:
                              MyMessageBoxes.ShowMessage().show_info("Guide yourself through the app using the "
                                                                     "tab bar at the top, there are many things to do."
                                                                     "\nAdmin users are also given extra tabs in their "
                                                                     "app."))

        # Logout Option
        main_bar.add_command(
            label='Logout',
            command=lambda: (self.root.destroy(), main_bar.delete("Logout"), LoginScreen.MainLogin(self.parent))
        )

    def change_background_colour(self, mode, bar):
        if mode == "Light":
            self.parent.configure(bg="white")
            ctk.set_appearance_mode("light")
        elif mode == "Dark":
            self.parent.configure(bg="black")
            ctk.set_appearance_mode("dark")

    def create_expense_label(self, parent, place_x, place_y):
        total_expenses_from_user = self.main_db.return_total_inputted_from_user(self.current_user)
        total_expenses_summed = self.main_db.return_expenses_summed(self.current_user)
        if self.main_db.check_user_level(self.current_user) == 0:
            self.expense_view_label = ctk.CTkLabel(parent, text=f"User {self.current_user}:\n"
                                                                f"{total_expenses_from_user} Expenses,"
                                                                f" Equating £"
                                                                f"{total_expenses_summed}.",
                                                   font=("Arial", 18))
        else:
            self.expense_view_label = ctk.CTkLabel(parent, text=f"Admin User {self.current_user}:\n"
                                                                f"{total_expenses_from_user} Total Expenses,"
                                                                f" Equating £{total_expenses_summed}",
                                                   font=("Arial", 18))
        self.expense_view_label.place(x=place_x, y=place_y)  # Adjust coordinates as needed

    def create_expenses_tab(self):
        # Access the "Expenses" tab directly
        expenses_tab = self.nb.tab("Expenses")

        #  Initialising the icons for widgets
        green_plus_image_path = "ProjectImages/GreenPlusImage.png"
        green_plus_image = Image.open(green_plus_image_path)
        green_plus_image = green_plus_image.resize((60, 60))  # Resize to fit button
        green_plus_image = ctk.CTkImage(light_image=green_plus_image, size=(60, 60))

        red_remove_image_path = "ProjectImages/RedRemoveImage.png"
        red_remove_image = Image.open(red_remove_image_path)
        red_remove_image = red_remove_image.resize((60, 60))  # Resize to fit button
        red_remove_image = ctk.CTkImage(light_image=red_remove_image, size=(60, 60))

        download_file_image_path = "ProjectImages/DownloadFileImage.png"
        download_file_image = Image.open(download_file_image_path)
        download_file_image = download_file_image.resize((60, 60))  # Resize to fit button
        download_file_image = ctk.CTkImage(light_image=download_file_image, size=(60, 60))

        spreadsheet_image_path = "ProjectImages/SpreadsheetImage.png"
        spreadsheet_image = Image.open(spreadsheet_image_path)
        spreadsheet_image = spreadsheet_image.resize((60, 60))  # Resize to fit button
        spreadsheet_image = ctk.CTkImage(light_image=spreadsheet_image, size=(60, 60))

        # Add Expense button
        self.create_expense_label(expenses_tab, 300, 20)
        self.add_expenses_button = ctk.CTkButton(expenses_tab, image=green_plus_image, command=self.add_expense,
                                                 width=200, height=100, text="Add Expense", compound="bottom",
                                                 font=("Arial", 16))
        self.add_expenses_button.place(x=175, y=100)

        # View Expenses button
        self.remove_expenses_button = ctk.CTkButton(expenses_tab, image=red_remove_image, command=self.remove_expense,
                                                    width=200, height=100, text="Remove Expense(s)", compound="bottom",
                                                    font=("Arial", 16))
        self.remove_expenses_button.place(x=450, y=100)

        # Remove Expense button
        self.view_expenses_button = ctk.CTkButton(expenses_tab, image=spreadsheet_image, command=self.view_expenses,
                                                  width=200, height=100, text="Download Expenses",
                                                  compound="bottom", font=("Arial", 16))
        self.view_expenses_button.place(x=175, y=250)

        self.edit_expense_button = ctk.CTkButton(expenses_tab, image=download_file_image,
                                                 command=self.edit_expense, width=200, height=100,
                                                 text="Edit Expense", compound="bottom", font=("Arial", 16))
        self.edit_expense_button.place(x=450, y=250)

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
        self.name_entry = ctk.CTkEntry(self.add_expense_frame)
        self.name_entry.place(x=200, y=60)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, self.name_entry, "Name")

        quantity_label = ctk.CTkLabel(self.add_expense_frame, text="Quantity purchased:")
        quantity_label.place(x=50, y=95)
        self.quantity_entry = ctk.CTkEntry(self.add_expense_frame)
        self.quantity_entry.place(x=200, y=95)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, self.quantity_entry, "Quantity")

        price_label = ctk.CTkLabel(self.add_expense_frame, text="Price per unit:")
        price_label.place(x=50, y=130)
        self.price_entry = ctk.CTkEntry(self.add_expense_frame)
        self.price_entry.place(x=200, y=130)
        MyCustomFunctions.EntryPlaceHolderText(self.add_expense_frame, self.price_entry, "Price")

        type_label = ctk.CTkLabel(self.add_expense_frame, text="Item type:")
        type_label.place(x=50, y=165)
        type_options = ["Rent", "Utilities", "Salaries", "Insurance", "Equipment", "Supplies", "Marketing", "Services",
                        "Training", "Travel", "Food", "Other"]
        self.type_option_menu = ctk.CTkOptionMenu(self.add_expense_frame, values=type_options)
        self.type_option_menu.set("Type:")
        self.type_option_menu.place(x=200, y=165)

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
                                      width=140, command=lambda: (self.add_expense_window.withdraw(),
                                                                  self.submit_expense_db([
                                                                      self.name_entry.get(), self.quantity_entry.get(),
                                                                      self.price_entry.get(),
                                                                      self.type_option_menu.get()], [
                f"{MyDatabase.AccountsDatabase().return_total_expense_amount() + 1:06d}",  # Auto-generate ExpenseID
                self.current_user,  # Use the current user ID
                self.name_entry.get(),
                self.quantity_entry.get(),
                self.price_entry.get(),
                self.type_option_menu.get(),
                datetime.now().strftime('%Y-%m-%d')], self.add_expense_window)))
        submit_button.place(x=200, y=240)

        self.add_expense_window.mainloop()

    def submit_expense_db(self, default_inputs, submitted_inputs, parent):
        # Gather inputs
        parent.withdraw()
        placeholders = ["Name", "Quantity", "Price", "Type:"]
        invalid_fields = [
            placeholder for placeholder, value in zip(placeholders, default_inputs)
            if not str(value).strip() or value == placeholder
        ]

        # Validate inputs
        if invalid_fields:
            MyMessageBoxes.ShowMessage().show_error(
                f"Ensure the following fields are filled correctly:\n{', '.join(invalid_fields)}."
            )
            parent.deiconify()
            return

        # Try to submit the expense to the database
        try:
            self.main_db.submit_expense_db(submitted_inputs)
            MyMessageBoxes.ShowMessage().show_info("Expense added successfully.")
            self.show_main_window()  # Navigate back to the main window
        except Exception as error:
            MyMessageBoxes.ShowMessage().show_info(f"An error occurred: {error}")
            parent.deiconify()

    def remove_expense(self):
        # Create a new CTk window
        self.remove_main_window()
        self.remove_expense_window = ctk.CTk()
        self.remove_expense_frame = ctk.CTkFrame(self.remove_expense_window)
        self.remove_expense_frame.pack(expand=True, fill="both")
        self.remove_expense_window.title("Remove Expense(s)")
        self.remove_expense_window.geometry("620x383+640+200")  # Customize the size
        self.remove_expense_window.resizable(False, False)
        self.remove_expense_label = ctk.CTkLabel(self.remove_expense_window, text='Remove Expense(s):')

        # Pass the callback function (show_main_window) to ExpenseViewer
        self.expense_spreadsheet = MyDatabase.ExpenseViewer(self.current_user, self.remove_expense_frame,
                                                            self.remove_expense_frame, lambda:
                                                            self.show_main_window(self.remove_expense_window))

        # Back button to go back to the main window
        back_button = ctk.CTkButton(self.remove_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.remove_expense_window), width=140)
        back_button.pack(expand=True, side='left')

        self.remove_expense_window.mainloop()

    def view_expenses(self):
        self.remove_main_window()
        self.view_expense_window = ctk.CTk()
        self.view_expense_frame = ctk.CTkFrame(self.view_expense_window)
        self.view_expense_frame.pack(expand=True, fill="both")
        self.view_expense_window.title("View Expenses")
        self.view_expense_window.geometry("750x463+475+125")
        self.excel_expense_spreadsheet = MyDatabase.DisplayExcelSpreadsheet(self.current_user, self.view_expense_frame)
        back_button = ctk.CTkButton(self.view_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.view_expense_window), width=200)
        back_button.pack(padx=30, side='left')
        download_button = ctk.CTkButton(self.view_expense_frame, text="Download",
                                        command=lambda: self.export_expenses(), width=200)
        download_button.pack(padx=30, side='right')
        self.view_expense_window.mainloop()

    def export_expenses(self):
        self.remove_main_window()
        download_table = MyMessageBoxes.ShowMessage.ask_question("Select which year's expenses you want to"
                                                                 " download",
                                                                 "All years", "Previous year",
                                                                 "Back", "Back")
        if download_table == "All years":
            try:
                self.view_expense_window.destroy()
                MyDatabase.DisplayExcelSpreadsheet(self.current_user, ctk.CTk()).download_expenses()
                MyMessageBoxes.ShowMessage.show_info("Spreadsheet downloaded successfully.")
                self.show_main_window(ctk.CTkToplevel())
            except Exception as error:
                MyMessageBoxes.ShowMessage.show_info(f"Something went wrong: {str(error)}")
        elif download_table == "Previous year":
            expenses = self.main_db.return_expenses_from_user(self.current_user)
            if not expenses:
                MyMessageBoxes.ShowMessage.show_info("No expenses found for this user.")
                return
            years = {datetime.strptime(str(expense['Date']), '%Y-%m-%d').year for expense in expenses}
            earliest_year = min(years)
            current_year = datetime.now().year
            year_toplevel = ctk.CTkToplevel()
            year_toplevel.geometry('+960+400')
            years_label = ctk.CTkLabel(year_toplevel, text=f"Found expenses from {earliest_year} - {current_year}")
            if earliest_year == current_year:
                years_label.configure(text=f"Found expenses from {earliest_year}")
            years_label.pack(expand=True, fill="both")
            year_choices_frame = ctk.CTkFrame(year_toplevel)
            year_choices_frame.pack(expand=True, fill="both")
            for year in range(earliest_year, current_year + 1):
                button = ctk.CTkButton(year_choices_frame, text=str(year),
                                       command=lambda: self.download_expenses_for_year(year, year_toplevel))
                button.grid(row=(year - earliest_year) // 5, column=(year - earliest_year) % 5, padx=10,
                            pady=10)  # Arrange in a grid
            cancel_button = ctk.CTkButton(year_toplevel, text="Back", command=lambda: (year_toplevel.destroy(),
                                                                                       self.export_expenses()))
            cancel_button.pack(expand=True, fill="both")

    def edit_expense(self):
        self.remove_main_window()
        self.edit_expense_window = ctk.CTk()
        self.edit_expense_frame = ctk.CTkFrame(self.edit_expense_window)
        self.edit_expense_frame.pack(expand=True, fill="both")
        self.edit_expense_window.title("Edit Expenses")
        self.edit_expense_window.geometry("750x463+585+125")
        self.edit_expense_window.resizable(False, False)
        self.editing_spreadsheet = MyDatabase.ExpenseEditor(self.current_user, self.edit_expense_frame,
                                                            self.edit_expense_frame, show_expenses=True,
                                                            callback_function=lambda: self.show_main_window(
                                                                self.edit_expense_window))
        back_button = ctk.CTkButton(self.edit_expense_frame, text="Back",
                                    command=lambda: self.show_main_window(self.edit_expense_window), width=200)
        back_button.pack(padx=30, side='left')
        self.edit_expense_window.mainloop()

    def download_expenses_for_year(self, year, parent):
        try:
            MyDatabase.DisplayExcelSpreadsheet(self.current_user, ctk.CTk(), year).download_expenses()
            MyMessageBoxes.ShowMessage.show_info(f"Spreadsheet for {year} downloaded successfully.")
            self.show_main_window(parent)
        except Exception as error:
            MyMessageBoxes.ShowMessage.show_info(f"Something went wrong: {str(error)}")

    def create_graphs_tab(self):
        """
        Creates the 'Graphs' tab in the notebook, embedding matplotlib plots for data visualization.
        """
        graphs_tab = self.nb.tab("Graphs")
        graphs_tab_frame = ctk.CTkFrame(graphs_tab)
        graphs_tab_frame.pack(fill="both", expand=True)

        # Create a dedicated frame for the buttons at the top
        button_frame = ctk.CTkFrame(graphs_tab_frame)
        button_frame.pack(fill="x", pady=10)

        # Create a dedicated frame for the graph below the buttons
        plot_frame = ctk.CTkFrame(graphs_tab_frame)
        plot_frame.pack(fill="both", expand=True)

        # Variable to track the currently displayed graph
        current_graph = dict(name=str(), plot_func=type(any))
        current_year = ctk.StringVar()

        def clear_canvas():
            """Clears any existing canvas in the plot frame."""
            for widget in plot_frame.winfo_children():
                widget.destroy()

        def display_plot(fig):
            """Embeds a matplotlib figure into the plot frame."""
            clear_canvas()
            canvas = FigureCanvasTkAgg(fig, plot_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

        def plot_expenses_over_time():
            """Plots the daily expenses for the current user for a selected year."""
            current_graph["name"] = "expenses_over_time"
            current_graph["plot_func"] = plot_expenses_over_time
            clear_canvas()
            try:
                expenses = self.main_db.return_expenses_from_user(self.current_user)
                if not expenses:
                    raise ValueError("No expenses data available to plot.")

                # Extract the year from the current_year input (assuming it is a string in the format 'Year: YYYY')
                selected_year = int(current_year.get().strip("Year: "))

                # Aggregate expenses by date for the selected year
                aggregated_expenses = defaultdict(float)
                for expense in expenses:
                    # Extract year from the expense date and compare with selected year
                    expense_year = datetime.strptime(str(expense['Date']), '%Y-%m-%d').year
                    if expense_year != selected_year:
                        continue  # Skip expenses that do not match the selected year

                    # If the expense matches the selected year, aggregate it by date
                    date = datetime.strptime(str(expense['Date']), '%Y-%m-%d').date()
                    aggregated_expenses[date] += float(expense['Price']) * expense['Quantity']

                if not aggregated_expenses:
                    raise ValueError(f"No expenses found for the selected year: {selected_year}")

                # Sort the dates and create a list of total amounts for the sorted dates
                sorted_dates = sorted(aggregated_expenses.keys())
                total_amounts = [aggregated_expenses[date] for date in sorted_dates]

                # Create the matplotlib figure
                fig = Figure(figsize=(6, 4), dpi=100)
                fig.patch.set_facecolor('#cfcfcf')
                ax = fig.add_subplot(111)
                ax.plot(sorted_dates, total_amounts, marker='o', linestyle='-', color='b')

                # Customize the graph
                ax.set_title(f"Daily Expenses for {self.current_user} in {selected_year}", fontsize=14)
                ax.set_xlabel("Date", fontsize=12)
                ax.set_ylabel("Total Expense (£)", fontsize=12)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                fig.autofmt_xdate(rotation=45)

                display_plot(fig)
            except Exception as e:
                ctk.CTkLabel(plot_frame, text=f"Error: {e}", font=("Arial", 16)).pack(pady=10)

        def plot_expense_distribution():
            """Plots the distribution of expenses by type."""
            current_graph["name"] = "expense_distribution"
            current_graph["plot_func"] = plot_expense_distribution
            clear_canvas()
            try:
                data = self.main_db.get_expenses_by_type(self.current_user)  # Adjust query logic in DB
                if not data:
                    raise ValueError("No expense distribution data available.")

                # Dictionary to accumulate amounts for each type
                aggregated_data = {}
                selected_year = int(current_year.get().strip("Year: "))

                for expense in data:
                    if expense['Date'].year == int(current_year.get().strip("Year: ")):
                        expense_type = expense['Type']
                        if expense_type not in aggregated_data:
                            aggregated_data[expense_type] = 0
                        aggregated_data[expense_type] += expense['TotalAmount']

                if not aggregated_data:
                    raise ValueError(f"No expenses found for the selected year: {selected_year}")

                types = tuple(aggregated_data.keys())
                amounts = tuple(aggregated_data.values())

                fig = Figure(figsize=(6, 4), dpi=100)
                fig.patch.set_facecolor('#cfcfcf')
                ax = fig.add_subplot(111)
                ax.pie(amounts, labels=types, autopct='%1.1f%%', startangle=140)
                ax.set_title("Expense Distribution by Type", fontsize=14)

                display_plot(fig)
            except Exception as e:
                ctk.CTkLabel(plot_frame, text=f"Error: {e}", font=("Arial", 16)).pack(pady=10)

        def plot_expense_heatmap():
            """Creates a heatmap to visualize expenses over the course of a year, with days of the month and months."""
            current_graph["name"] = "expense_heatmap"
            current_graph["plot_func"] = plot_expense_heatmap
            clear_canvas()
            try:
                expenses = self.main_db.return_expenses_from_user(self.current_user)
                if not expenses:
                    raise ValueError("No expenses data available for the heatmap.")

                # Aggregate expenses by month and day of the month
                aggregated_expenses = defaultdict(float)
                selected_year = int(current_year.get().strip("Year: "))

                for expense in expenses:
                    date = datetime.strptime(str(expense['Date']), '%Y-%m-%d').date()
                    if date.year == selected_year:  # Check if the expense matches the selected year
                        month = date.month  # Get the month (1 to 12)
                        day_of_month = date.day  # Get the day of the month (1 to 31)
                        aggregated_expenses[(month, day_of_month)] += float(expense['Price']) * expense['Quantity']

                if not aggregated_expenses:
                    raise ValueError(f"No expenses found for the selected year: {selected_year}")

                # Create a 2D matrix for the heatmap (31 days x 12 months)
                heatmap_data = np.zeros((31, 12))  # 31 rows (days of the month), 12 columns (months)
                for (month, day_of_month), total in aggregated_expenses.items():
                    heatmap_data[day_of_month - 1][month - 1] += total  # Map to the correct position

                # Create the heatmap
                fig = Figure(figsize=(16, 12), dpi=100)
                fig.patch.set_facecolor('#cfcfcf')
                ax = fig.add_subplot(111)
                sns.heatmap(
                    heatmap_data,
                    cmap="YlOrRd",
                    ax=ax,
                    cbar_kws={"label": "Money Spent Per Day"},
                    yticklabels=range(1, 32),  # Days 1 to 31
                    xticklabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                    # Month labels
                    linewidths=0.5,
                )
                ax.set_title("Expense Heatmap Over the Year", fontsize=14)
                ax.set_xlabel("Month of the Year", fontsize=12)
                ax.set_ylabel("Day of the Month", fontsize=12)
                ax.invert_yaxis()
                ax.tick_params(axis='y', labelrotation=0)
                display_plot(fig)
            except Exception as e:
                ctk.CTkLabel(plot_frame, text=f"Error: {e}", font=("Arial", 16)).pack(pady=10)

        def refresh_graphs():
            """Refreshes the currently displayed graph."""
            if current_graph["plot_func"]:
                current_graph["plot_func"]()
            else:
                ctk.CTkLabel(plot_frame, text="No graph to refresh.", font=("Arial", 16)).pack(pady=10)

        # Buttons for selecting graphs in the button_frame
        time_graph_button = ctk.CTkButton(button_frame, text="Money Spent Over Time Graph",
                                          command=plot_expenses_over_time)
        time_graph_button.pack(side="left", padx=6, expand=True, fill='both')

        distribution_graph_button = ctk.CTkButton(button_frame, text="Expense Type Pie Chart",
                                                  command=plot_expense_distribution)
        distribution_graph_button.pack(side="left", padx=6, expand=True, fill='both')

        heatmap_button = ctk.CTkButton(button_frame, text="Yearly Expense Heatmap",
                                       command=plot_expense_heatmap)
        heatmap_button.pack(side="left", padx=6, expand=True, fill='both')
        starting_year = datetime.now().year
        choose_year_button = ctk.CTkOptionMenu(button_frame, values=[f'Year: {starting_year - 1}',
                                                                     f'Year: {starting_year}',
                                                                     f'Year: {starting_year + 1}',
                                                                     f'Year: {starting_year + 2}'],
                                               variable=current_year)
        choose_year_button.set(f'Year: {starting_year}')
        choose_year_button.pack(side="left", padx=6, expand=True, fill='both')

        refresh_graph_button = ctk.CTkButton(button_frame, text="Refresh Graph",
                                             command=refresh_graphs)
        refresh_graph_button.pack(side="left", padx=6, expand=True, fill='both')

        # Default graph display
        plot_expenses_over_time()

    def create_table_tab(self):
        # Create the Table tab and its main frame
        table_tab = self.nb.tab("Table")
        table_tab_frame = ctk.CTkFrame(table_tab)
        control_frame = ctk.CTkFrame(table_tab_frame)

        # Create a frame for table controls (e.g., refresh button)
        table_tab_frame.pack(fill="both", expand=True)
        control_frame.pack(fill="x")

        # Create a frame for the table and scrollbars
        table_frame = ctk.CTkFrame(table_tab_frame)
        table_frame.pack(fill="both", expand=True)

        # Add vertical and horizontal scrollbars
        scrollbar_y = tk.Scrollbar(table_frame, orient="vertical")
        scrollbar_x = tk.Scrollbar(table_frame, orient="horizontal")

        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 12))  # Change "Helvetica" and 12 as needed
        style.configure("Treeview.Heading", font=("Roboto", 13))

        # Create the Treeview widget for displaying the table
        tree = ttk.Treeview(
            table_frame,
            columns=("ExpenseID", "UserID", "Name", "Type", "Quantity", "Price", "Date"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )

        # Configure scrollbar actions
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)

        # Place the scrollbars and the treeview in the frame
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        # Define table headers
        headers = ["ExpenseID", "UserID", "Name", "Type", "Quantity", "Price", "Date"]
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True, width=100)

        def fetch_table_data():
            """
            Fetches data from the database and populates the table.
            """
            # Clear the table
            tree.delete(*tree.get_children())

            try:
                # Retrieve data from the database
                if self.main_db.check_user_level(self.current_user) == 0:
                    expenses = self.main_db.return_expenses_from_user(self.current_user)
                else:
                    expenses = self.main_db.return_all_expenses()

                if not expenses:
                    raise ValueError("No data available to display.")

                # Insert rows into the Treeview
                for row in expenses:
                    if isinstance(row, dict):  # Ensure each row is a dictionary
                        tree.insert(
                            "", "end",
                            values=(
                                row.get("ExpenseID", ""),
                                row.get("UserID", ""),
                                row.get("Name", ""),
                                row.get("Type", "Unknown"),  # Use 'Unknown' if Type is missing
                                row.get("Quantity", 0),
                                f"£{row.get('Price', 0):.2f}",
                                row.get("Date", ""),
                            ),
                        )
            except Exception as e:
                return f"Error loading data into table: {e}"

        def refresh_table():
            """
            Refreshes the table to display the latest data.
            """
            fetch_table_data()

        current_user_label = ctk.CTkLabel(control_frame, text=f"User {self.current_user}'s Expenses:" if self.main_db.
                                          check_user_level(self.current_user) == 0 else "All Expenses:")
        current_user_label.pack(side="bottom", expand=True)
        # Add Refresh Button to control frame
        refresh_button = ctk.CTkButton(control_frame, text="Refresh Table", command=refresh_table)
        refresh_button.pack(side="top", expand=True)

        # Fetch and display data initially
        fetch_table_data()

    def create_predictor_tab(self):
        """
        Creates the 'Plotter' tab in the notebook to predict future
        expenses using historical data and display them on a graph.
        """

        # Create the Plotter tab and its main frame
        plotter_tab = self.nb.tab("Predictor")
        plotter_tab_frame = ctk.CTkFrame(plotter_tab)
        plotter_tab_frame.pack(fill="both", expand=True)

        predict_button = ctk.CTkButton(plotter_tab_frame, text="Refresh Future Expenses Prediction")
        predict_button.pack()

        # Create a frame for the graph
        graph_frame = ctk.CTkFrame(plotter_tab_frame)
        graph_frame.pack(fill="both", expand=True)

        def clear_canvas():
            """Clears any existing canvas in the graph frame."""
            for widget in graph_frame.winfo_children():
                widget.destroy()

        def display_plot(fig):
            """Embeds a matplotlib figure into the graph frame."""
            clear_canvas()
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

        def fetch_and_predict_expenses():
            """
            Fetches historical expense data, trains a machine learning model, and predicts future expenses.
            """
            try:
                # Retrieve historical data from the database
                expenses = self.main_db.return_expenses_from_user(self.current_user)

                if not expenses:
                    raise ValueError("No historical data available to predict future expenses.")

                # Prepare data for the model
                dates = []
                amounts = []
                for expense in expenses:
                    # Parse date and convert it to datetime
                    date = datetime.strptime(str(expense['Date']), '%Y-%m-%d')
                    dates.append(
                        (date - datetime(1970, 1, 1)).days)  # Convert date to numerical format (days since epoch)
                    amounts.append(float(expense['Price']) * expense['Quantity'])

                dates = np.array(dates).reshape(-1, 1)  # Reshape for scikit-learn
                amounts = np.array(amounts)

                # Split the data into training and test sets
                X_train, X_test, y_train, y_test = train_test_split(dates, amounts, test_size=0.2, random_state=42)

                # Train a linear regression model
                model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
                model.fit(X_train, y_train)

                # Predict future expenses
                future_dates = np.array(
                    [(datetime.today() + timedelta(days=i) - datetime(1970, 1, 1)).days for i in range(1, 31)]
                ).reshape(-1, 1)  # Predict for the next 30 days
                future_expenses = model.predict(future_dates)
                future_expenses = np.maximum(future_expenses, 0)
                # Create a matplotlib figure for plotting
                fig = Figure(figsize=(8, 5), dpi=100)
                fig.patch.set_facecolor('#cfcfcf')
                ax = fig.add_subplot(111)

                # Plot historical data
                ax.plot(
                    [datetime(1970, 1, 1) + timedelta(days=int(d[0])) for d in dates],
                    amounts,
                    label="Historical Data",
                    marker='o',
                    linestyle='-',
                    color='blue'
                )

                # Plot predicted future expenses
                future_dates_readable = [
                    (datetime(1970, 1, 1) + timedelta(days=int(d[0]))).strftime('%Y-%m-%d') for d in future_dates
                ]
                ax.plot(
                    [datetime.strptime(d, '%Y-%m-%d') for d in future_dates_readable],
                    future_expenses,
                    label="Predicted Future Expenses",
                    marker='x',
                    linestyle='--',
                    color='red'
                )

                # Customize the graph
                ax.set_title("Expense Prediction for the Next 30 Days", fontsize=14)
                ax.set_xlabel("Date", fontsize=12)
                ax.set_ylabel("Expense Amount (£)", fontsize=12)
                ax.legend()
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                fig.autofmt_xdate(rotation=45)

                # Display the graph
                display_plot(fig)

            except Exception as e:
                clear_canvas()
                ctk.CTkLabel(graph_frame, text=f"Error: {e}", font=("Arial", 16)).pack(pady=10)

        # Create a button to trigger the prediction

        predict_button.configure(command=fetch_and_predict_expenses)
        # Display the initial empty graph
        fetch_and_predict_expenses()


class AdminWindow(DefaultWindow):
    def __init__(self, parent, current_user, current_tab=None):
        super().__init__(parent, current_user)
        self.nb.add("Accounts")
        self.nb.add("Budgeting")
        self.nb.add("Database")
        self.nb.set(current_tab) if current_tab else None
        self.setup_extra_tabs()

    def setup_extra_tabs(self):
        self.create_accounts_tab()
        self.create_budgeting_tab()
        self.create_database_tab()

    def create_accounts_tab(self):
        accounts_tab = self.nb.tab("Accounts")

        add_user_image_path = "ProjectImages/AddUserImage.png"
        add_user_image = Image.open(add_user_image_path)
        add_user_image = add_user_image.resize((60, 60))  # Resize to fit button
        add_user_image = ctk.CTkImage(light_image=add_user_image, size=(80, 75))

        remove_user_image_path = "ProjectImages/RemoveUserImage.png"
        remove_user_image = Image.open(remove_user_image_path)
        remove_user_image = remove_user_image.resize((60, 60))
        remove_user_image = ctk.CTkImage(light_image=remove_user_image, size=(80, 75))

        edit_user_image_path = "ProjectImages/EditUserImage.png"
        edit_user_image = Image.open(edit_user_image_path)
        edit_user_image = edit_user_image.resize((60, 60))
        edit_user_image = ctk.CTkImage(light_image=edit_user_image, size=(80, 75))

        view_users_image_path = "ProjectImages/ViewUsersImage.png"
        view_users_image = Image.open(view_users_image_path)
        view_users_image = view_users_image.resize((60, 60))
        view_users_image = ctk.CTkImage(light_image=view_users_image, size=(80, 75))

        add_user_button = ctk.CTkButton(accounts_tab, image=add_user_image, command=self.add_new_user,
                                        width=200, height=100, text="Add User", compound="bottom",
                                        font=("Arial", 16))
        add_user_button.place(x=175, y=100)

        remove_user_button = ctk.CTkButton(accounts_tab, image=remove_user_image, command=self.remove_user,
                                           width=200, height=100, text="Remove User", compound="bottom",
                                           font=("Arial", 16))
        remove_user_button.place(x=450, y=100)

        view_users_button = ctk.CTkButton(accounts_tab, image=view_users_image, command=self.view_users,
                                          width=200, height=100, text="View Users", compound="bottom",
                                          font=("Arial", 16))
        view_users_button.place(x=175, y=250)

        edit_user_button = ctk.CTkButton(accounts_tab, image=edit_user_image, command=self.edit_user,
                                         width=200, height=100, text="Edit User", compound="bottom",
                                         font=("Arial", 16))
        edit_user_button.place(x=450, y=250)

    def add_new_user(self):
        self.root.destroy()
        CreateAccountScreen.CreateAccount(self.parent, self.current_user)

    def remove_user(self):
        self.remove_main_window()
        self.remove_user_window = ctk.CTk()
        self.remove_user_frame = ctk.CTkFrame(self.remove_user_window)
        self.remove_user_frame.pack(expand=True, fill="both")
        self.remove_user_window.resizable(False, False)
        self.remove_user_window.title("Remove User(s)")
        self.remove_user_window.geometry("850x525+475+125")
        self.user_spreadsheet = MyDatabase.ExpenseViewer(self.current_user, self.remove_user_frame,
                                                         self.remove_user_frame,
                                                         lambda: self.show_main_window(self.remove_user_window),
                                                         True)
        back_button = ctk.CTkButton(self.remove_user_frame, text="Back",
                                    command=lambda: self.show_main_window(self.remove_user_window), width=140)
        back_button.pack(expand=True, side='left')

        self.remove_user_window.mainloop()

    def edit_user(self):
        self.remove_main_window()
        self.edit_user_window = ctk.CTk()
        self.edit_user_frame = ctk.CTkFrame(self.edit_user_window)
        self.edit_user_frame.pack(expand=True, fill="both")
        self.edit_user_window.geometry("750x463+635+125")
        self.edit_user_window.resizable(False, False)
        self.edit_user_window.title("Edit User(s)")
        self.edit_user_spreadsheet = MyDatabase.ExpenseEditor(self.current_user, self.edit_user_frame,
                                                              self.edit_user_frame, show_users=True,
                                                              callback_function=lambda:
                                                              (self.show_main_window(self.edit_user_window)))
        back_button = ctk.CTkButton(self.edit_user_frame, text="Back",
                                    command=lambda: self.show_main_window(self.edit_user_window), width=200)
        back_button.pack(padx=30, side='left')
        self.edit_user_window.mainloop()

    def view_users(self):
        self.remove_main_window()
        self.view_users_window = ctk.CTk()
        self.view_users_frame = ctk.CTkFrame(self.view_users_window)
        self.view_users_frame.pack(expand=True, fill="both")
        self.view_users_window.title("View Users")
        self.view_users_window.geometry("1000x500+475+125")
        self.view_users_window.resizable(False, False)
        MyDatabase.DisplayExcelSpreadsheet(self.current_user, self.view_users_frame, year=None, show_users=True)
        back_button = ctk.CTkButton(self.view_users_frame, text="Back",
                                    command=lambda: self.show_main_window(self.view_users_window), width=140)
        back_button.pack(expand=True, side='left')
        self.view_users_window.mainloop()

    def create_budgeting_tab(self):
        budgeting_tab = self.nb.tab("Budgeting")
        expense_vs_income_button = ctk.CTkButton(budgeting_tab, command=self.expense_vs_income, width=200,
                                                 height=100, text="Expense Against Income", font=("Arial", 16))
        expense_vs_income_button.place(x=175, y=100)
        currency_converter_button = ctk.CTkButton(budgeting_tab, command=self.currency_converter, width=200,
                                                  height=100, text="Currency Converter", font=("Arial", 16))
        currency_converter_button.place(x=450, y=250)
        income_graph_button = ctk.CTkButton(budgeting_tab, command=lambda: (self.income_graph(
            self.main_db.return_all_incomes())), width=200, height=100, text="Income Graph", font=("Arial", 16))
        income_graph_button.place(x=450, y=100)
        loan_calculator_button = ctk.CTkButton(budgeting_tab, command=self.display_calculators, width=200, height=100,
                                               text="Calculators", font=("Arial", 16))
        loan_calculator_button.place(x=175, y=250)

    def expense_vs_income(self):
        self.remove_main_window()
        expense_income_window = ctk.CTk()
        expense_income_window.geometry("800x494+560+200")
        expense_income_window.resizable(False, False)
        expense_income_buttons_frame = ctk.CTkFrame(expense_income_window)
        expense_income_buttons_frame.pack(fill='both', side='bottom')
        expense_vs_income_frame = ctk.CTkFrame(expense_income_window)
        expense_vs_income_frame.pack(fill="both", expand=True, pady=5)

        def display_plot():
            for widget in expense_vs_income_frame.winfo_children():
                widget.destroy()

            try:
                # Retrieve and process expenses
                expenses = self.main_db.return_all_expenses()
                expense_totals = {}

                for expense in expenses:
                    date = expense["Date"]  # Already a datetime.date object
                    total_price = expense["Quantity"] * expense["Price"]
                    expense_totals[date] = expense_totals.get(date, 0) + total_price

                expense_dates = [datetime.combine(date, datetime.min.time()) for date in expense_totals.keys()]
                expense_values = list(expense_totals.values())

                # Retrieve and process incomes
                incomes = self.main_db.return_all_incomes()
                income_totals = {}

                for income in incomes:
                    # Placeholder logic for income dates
                    date = datetime.now().date()  # Replace with actual date logic if available
                    salary = income["Salary"]
                    income_totals[date] = income_totals.get(date, 0) + salary

                income_dates = [datetime.combine(date, datetime.min.time()) for date in income_totals.keys()]
                income_values = list(income_totals.values())

                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size

                # Plot Expenses
                ax.plot(expense_dates, expense_values, label="Expenses", marker='o', color="red")

                # Add Horizontal Line for Income
                income_mean = sum(income_values) / len(income_values)  # Average income if multiple
                ax.hlines(
                    y=income_mean,
                    xmin=min(expense_dates),
                    xmax=max(expense_dates),
                    colors='green',
                    label='Income'
                )

                # Title and Labels
                ax.set_title("Expenses vs Income", fontsize=16)
                ax.set_xlabel("Date")
                ax.set_ylabel("Amount")
                ax.legend()
                ax.grid(True)

                # Adjust Font Size and Rotate Dates
                ax.tick_params(axis='x', labelsize=8)  # Smaller font size for x-axis
                fig.autofmt_xdate(rotation=45)  # Rotate date labels for better visibility

                # Display
                canvas = FigureCanvasTkAgg(fig, master=expense_vs_income_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(expand=True, fill="both")
                canvas.draw()

            except Exception as e:
                error_label = ctk.CTkLabel(expense_vs_income_frame, text=f"Error: {e}")
                error_label.pack(pady=20)

        # Add a button to refresh or redraw the plot
        display_plot()
        refresh_button = ctk.CTkButton(
            expense_income_buttons_frame,
            text="Refresh Expenses Against Income",
            command=display_plot
        )
        refresh_button.pack(pady=10, expand=True, side='right')
        back_button = ctk.CTkButton(
            expense_income_buttons_frame,
            text="Back",
            command=lambda: self.show_main_window(expense_income_window)
        )
        back_button.pack(pady=10, expand=True, side='left')

        expense_income_window.mainloop()

    def currency_converter(self):
        # Remove the main window and create the converter window
        self.remove_main_window()
        converter_window = ctk.CTk()
        converter_window.geometry("400x300+760+200")
        converter_window.title("Currency Converter")

        # Frame for the converter UI
        converter_frame = ctk.CTkFrame(converter_window)
        converter_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Label for title
        title_label = ctk.CTkLabel(converter_frame, text="Currency Converter", font=("Arial", 16))
        title_label.pack(pady=10)

        # Input field for amount
        amount_entry = ctk.CTkEntry(converter_frame, placeholder_text="Enter amount")
        amount_entry.pack(pady=5)

        # Dropdown for source currency
        source_currency_var = ctk.StringVar(value="GBP")  # Default currency
        all_currencies = self.get_exchange_rates("GBP")  # Get all currencies from API
        if "error" in all_currencies:
            return f"Error fetching currencies: {all_currencies['error']}"

        # Get the list of all available currencies
        available_currencies = list(all_currencies.keys())

        # Popular currencies to show at the top
        default_currencies = ["GBP", "EUR", "USD"]

        # Remove popular currencies from the list of available currencies if they exist
        available_currencies = [currency for currency in available_currencies if currency not in default_currencies]

        # Combine popular currencies with the other currencies
        combined_currencies = default_currencies + available_currencies

        # Source currency dropdown with popular currencies at the top
        source_currency_menu = ctk.CTkOptionMenu(converter_frame, values=combined_currencies,
                                                 variable=source_currency_var)
        source_currency_menu.pack(pady=5)

        # Dropdown for target currency
        target_currency_var = ctk.StringVar(value="USD")  # Default currency
        target_currency_menu = ctk.CTkOptionMenu(converter_frame, values=combined_currencies,
                                                 variable=target_currency_var)
        target_currency_menu.pack(pady=5)

        # Label to display the result
        result_label = ctk.CTkLabel(converter_frame, text="", font=("Arial", 14))
        result_label.pack(pady=10)

        # Convert button
        def convert_currency():
            try:
                amount = float(amount_entry.get())  # Get the amount
                if amount < 0:
                    raise ValueError
                source_currency = source_currency_var.get()
                target_currency = target_currency_var.get()

                # Fetch real-time exchange rates
                rates = self.get_exchange_rates(source_currency)  # API call for real-time rates
                if source_currency not in rates or target_currency not in rates:
                    result_label.configure(text="Error: Invalid currency code")
                    return

                # Perform conversion
                conversion_rate = rates[target_currency]
                converted_amount = amount * conversion_rate
                result_label.configure(text=f"{amount} {source_currency} = {converted_amount:.2f} {target_currency}")

            except ValueError:
                result_label.configure(text="Error: Invalid amount")

        back_button = ctk.CTkButton(converter_frame, text="Back", command=lambda: self.show_main_window(
            converter_window))
        convert_button = ctk.CTkButton(converter_frame, text="Convert", command=convert_currency)
        back_button.pack(pady=10, expand=True, side='left')
        convert_button.pack(pady=10, expand=True, side='right')

        converter_window.mainloop()

    # Function to fetch exchange rates from the API
    def get_exchange_rates(self, base_currency):
        try:
            url = f"https://v6.exchangerate-api.com/v6/92eae0a0ef89c59477c0f99d/latest/{base_currency}"
            response = requests.get(url)
            data = response.json()

            if data['result'] == 'success':
                return data['conversion_rates']  # Returns the conversion rates
            else:
                raise Exception("Error fetching exchange rates")
        except Exception as e:
            return {"error": str(e)}  # Return error message in case of failure

    def income_graph(self, incomes):
        def refresh_graph():
            income_window.withdraw()
            income_window.quit()
            self.income_graph(self.main_db.return_all_incomes())

        self.remove_main_window()
        income_window = ctk.CTk()
        income_window.geometry("600x500+550+200")
        income_window.title("Income Graph")

        # Create a frame for the graph
        graph_frame = ctk.CTkFrame(income_window)
        graph_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Prepare data for the graph
        user_ids = [income['UserID'] for income in incomes]
        salaries = [income['Salary'] for income in incomes]
        levels = [income['Level'] for income in incomes]

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(user_ids, salaries, color='skyblue', edgecolor='black')

        for bar, level in zip(bars, levels):
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
                bar.get_height() / 2,  # Y position (middle of the bar)
                f'{level}',  # Text (level value)
                ha='center', va='center',  # Center alignment
                fontsize=10, color='black',  # Font size and color
                weight='bold'  # Bold text for visibility
            )
        # Customize the graph
        ax.set_title("Income by User", fontsize=16)
        ax.set_xlabel("UserID", fontsize=12)
        ax.set_ylabel("Salary", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Back and Refresh Buttons
        back_button = ctk.CTkButton(income_window, text="Back", command=lambda: self.show_main_window(income_window))
        refresh_button = ctk.CTkButton(income_window, text="Refresh Graph", command=refresh_graph)

        back_button.pack(padx=10, pady=10, expand=True, side='left')
        refresh_button.pack(padx=10, pady=10, expand=True, side='right')

        income_window.mainloop()

    def display_calculators(self):
        self.remove_main_window()
        calculators_window = ctk.CTk()
        calculators_window.title("Calculators")
        calculators_window.geometry("400x247+550+200")
        calculators_frame = ctk.CTkFrame(calculators_window)
        calculators_frame.pack(fill="both", expand=True)
        loan_calculator_button = ctk.CTkButton(calculators_frame, text="Loan calculator", command=lambda: (
            calculators_window.withdraw(), self.loan_calculator()))
        loan_calculator_button.pack(expand=True, fill='both', side='left', padx=10, pady=10)
        budgeting_calculator_button = ctk.CTkButton(calculators_frame, text="Budgeting calculator", command=lambda: (
            calculators_window.withdraw(), self.budgeting_calculator()))
        budgeting_calculator_button.pack(expand=True, fill='both', side='right', padx=10, pady=10)

        back_button = ctk.CTkButton(calculators_window, text="Back", width=100, command=lambda: self.show_main_window(
            calculators_window))
        back_button.pack(padx=10, pady=10, side='left')
        calculators_window.mainloop()

    def loan_calculator(self):
        loan_window = ctk.CTk()
        loan_window.geometry("517x320+550+200")
        loan_window.title("Loan Calculator")

        # Frame for the loan calculator UI
        loan_frame = ctk.CTkFrame(loan_window)
        loan_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        title_label = ctk.CTkLabel(loan_frame, text="Loan Calculator", font=("Arial", 16))
        title_label.pack(pady=10)

        # Entry for Loan Amount
        loan_amount_entry = ctk.CTkEntry(loan_frame, width=160)
        MyCustomFunctions.EntryPlaceHolderText(loan_frame, loan_amount_entry, "Loan Amount")
        loan_amount_entry.pack(pady=5)

        # Entry for Annual Interest Rate
        interest_rate_entry = ctk.CTkEntry(loan_frame, width=160)
        MyCustomFunctions.EntryPlaceHolderText(loan_frame, interest_rate_entry, "Annual Interest Rate (%)")
        interest_rate_entry.pack(pady=5)

        # Entry for Loan Term (in months)
        loan_term_entry = ctk.CTkEntry(loan_frame, width=160)
        MyCustomFunctions.EntryPlaceHolderText(loan_frame, loan_term_entry, "Loan Term (Months)")
        loan_term_entry.pack(pady=5)

        # Result Labels
        monthly_payment_label = ctk.CTkLabel(loan_frame, text="Monthly Payment: -", font=("Arial", 14))
        monthly_payment_label.pack(pady=5)

        total_payment_label = ctk.CTkLabel(loan_frame, text="Total Payment: -", font=("Arial", 14))
        total_payment_label.pack(pady=5)

        # Calculate Button
        def calculate_loan():
            try:
                # Get user inputs
                loan_amount = float(loan_amount_entry.get())
                annual_interest_rate = float(interest_rate_entry.get()) / 100  # Convert % to decimal
                loan_term_months = int(loan_term_entry.get())

                # Monthly Interest Rate
                monthly_interest_rate = annual_interest_rate / 12

                # Loan formula: M = P * r * (1 + r)^n / [(1 + r)^n - 1]
                numerator = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_months)
                denominator = ((1 + monthly_interest_rate) ** loan_term_months) - 1

                # Monthly payment
                monthly_payment = numerator / denominator if denominator != 0 else 0

                # Total payment
                total_payment = monthly_payment * loan_term_months

                # Update result labels
                monthly_payment_label.configure(text=f"Monthly Payment: {monthly_payment:.2f}")
                total_payment_label.configure(text=f"Total Payment: {total_payment:.2f}")

            except ValueError:
                # Handle invalid inputs
                monthly_payment_label.configure(text="Error: Invalid Input")
                total_payment_label.configure(text="")

        back_button = ctk.CTkButton(loan_frame, text="Back", command=lambda: (loan_window.withdraw(),
                                                                              self.display_calculators()))
        calculate_button = ctk.CTkButton(loan_frame, text="Calculate", command=calculate_loan)
        back_button.pack(pady=10, padx=15, side='left', expand=True)
        calculate_button.pack(pady=10, padx=15, side='right', expand=True)

        loan_window.mainloop()

    def budgeting_calculator(self):
        self.remove_main_window()
        budget_window = ctk.CTk()
        budget_window.geometry("500x400+550+200")
        budget_window.title("Budget Calculator")

        def get_monthly_expenses():
            expenses = self.main_db.return_all_expenses()
            monthly_totals = defaultdict(Decimal)  # Dictionary to store monthly totals
            for expense in expenses:
                expense_month = expense['Date'].strftime('%Y-%m')  # Get year-month as string
                monthly_totals[expense_month] += expense['Quantity'] * expense['Price']  # Add total for this expense

            # Step 2: Calculate average monthly expense for the current year
            current_year = date.today().year
            year_months = [month for month in monthly_totals if month.startswith(str(current_year))]
            if year_months:
                average_monthly_expense = sum(monthly_totals[month] for month in year_months) / len(year_months)
            else:
                average_monthly_expense = 0  # Handle no expenses case
            return average_monthly_expense

        # Frame for the budget calculator UI
        budget_frame = ctk.CTkFrame(budget_window)
        budget_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        title_label = ctk.CTkLabel(budget_frame, text="Budget Calculator", font=("Arial", 16))
        title_label.pack(pady=10)

        # Entry for Target Budget
        target_budget_entry = ctk.CTkEntry(budget_frame, width=160)
        MyCustomFunctions.EntryPlaceHolderText(budget_frame, target_budget_entry, "Target Budget Per Month")
        target_budget_entry.pack(pady=10)

        # Result Labels
        average_expenses_label = ctk.CTkLabel(budget_frame, text=f"Average Monthly Expenses: {get_monthly_expenses()}",
                                              font=("Arial", 14))
        average_expenses_label.pack(pady=10)

        target_result_label = ctk.CTkLabel(budget_frame, text="Target Status:", font=("Arial", 14))
        target_result_label.pack(pady=10)

        def calculate_budget():
            average_monthly_expense = get_monthly_expenses()

            # Step 3: Compare with user target
            try:
                target_budget = float(target_budget_entry.get())
                if average_monthly_expense < target_budget:
                    target_status = "Within budget"
                elif average_monthly_expense == target_budget:
                    target_status = "On budget"
                else:
                    target_status = "Over Budget"
            except ValueError:
                target_status = "Invalid Target Entered"

            # Update Result Labels
            average_expenses_label.configure(text=f"Average Monthly Expenses: {average_monthly_expense:.2f}")
            target_result_label.configure(text=f"Target Status: {target_status}")

        # Calculate Button
        calculate_button = ctk.CTkButton(budget_frame, text="Calculate", command=calculate_budget)
        calculate_button.pack(pady=20, side='right', expand=True)
        back_button = ctk.CTkButton(budget_frame, text="Back", command=lambda: (budget_window.withdraw(),
                                                                                self.display_calculators()))
        back_button.pack(pady=20, side='left', expand=True)

        budget_window.mainloop()

    def create_database_tab(self):
        database_tab = self.nb.tab("Database")
        add_test_data_button = ctk.CTkButton(database_tab, command=self.add_test_data,
                                             width=200, height=100, text="Add Test Data",
                                             font=("Arial", 16))
        add_test_data_button.place(x=175, y=100)
        import_data_button = ctk.CTkButton(database_tab, command=self.import_data,
                                           width=200, height=100, text="Import Data",
                                           font=("Arial", 16))
        import_data_button.place(x=450, y=100)
        show_database_structure_button = ctk.CTkButton(database_tab, command=self.display_database_structure,
                                                       width=200, height=100, text="Database Structure",
                                                       font=("Arial", 16))
        show_database_structure_button.place(x=175, y=250)
        wipe_database_button = ctk.CTkButton(database_tab, command=self.wipe_database,
                                             width=200, height=100, text="Wipe Database",
                                             font=("Arial", 16))
        wipe_database_button.place(x=450, y=250)

    def display_database_structure(self):
        self.remove_main_window()
        db_window = ctk.CTkToplevel(self.parent)
        db_window.geometry("800x600+550+200")
        db_window.title("Database Structure Viewer")

        def generate_schema():
            # Step 1: Define database URL and output file
            db_url = "mysql+mysqlconnector://expensedatabase:&FNBra!4117LVv@db4free.net/expensedatabase"
            output_file = "ProjectImages/DatabaseStructure.png"

            # Step 2: Generate schema diagram using ERAlchemy
            try:
                subprocess.run(["eralchemy", "-i", db_url, "-o", output_file], check=True)
            except subprocess.CalledProcessError as e:
                return e
            # Load and display the image
            try:
                database_structure_image_path = output_file
                database_structure_image = Image.open(database_structure_image_path)
                database_structure_image = database_structure_image.resize((660, 440))
                database_structure_image = ctk.CTkImage(light_image=database_structure_image, size=(660, 440))
                img_label = ctk.CTkLabel(schema_frame, image=database_structure_image, text="")
                img_label.pack(fill="both", expand=True)
            except Exception as e:
                img_label.configure(text=f"Error displaying schema image: {e}")

        # Frame for database schema viewer
        schema_frame = ctk.CTkFrame(db_window)
        schema_frame.pack(fill="both", expand=True)

        # Title Label
        title_label = ctk.CTkLabel(schema_frame, text="Database Structure", font=("Arial", 16))
        title_label.pack(pady=10)

        # Generate schema on load
        generate_schema()

        # Back Button
        back_button = ctk.CTkButton(db_window, text="Back",
                                    command=lambda: (db_window.withdraw(), self.show_main_window()))
        back_button.pack(pady=10, padx=20, side='left')

        db_window.mainloop()

    def add_test_data(self):
        # Create a new CTk window
        self.remove_main_window()
        self.add_test_data_window = ctk.CTk()  # Or ctk.CTkToplevel(self.parent) to make it a child of the main window
        self.add_test_data_frame = ctk.CTkFrame(self.add_test_data_window)
        self.add_test_data_frame.pack(expand=True, fill="both")
        self.add_test_data_window.title("Add Test Data")
        self.add_test_data_window.geometry("400x300+700+200")  # Updated geometry

        # Labels and inputs
        name_label = ctk.CTkLabel(self.add_test_data_frame, text="Name:")
        name_label.place(x=20, y=20)
        name_entry = ctk.CTkEntry(self.add_test_data_frame, width=200)
        name_entry.place(x=150, y=20)
        MyCustomFunctions.EntryPlaceHolderText(self.add_test_data_frame, name_entry, "Name")

        quantity_label = ctk.CTkLabel(self.add_test_data_frame, text="Quantity:")
        quantity_label.place(x=20, y=60)
        quantity_entry = ctk.CTkEntry(self.add_test_data_frame, width=200)
        quantity_entry.place(x=150, y=60)
        MyCustomFunctions.EntryPlaceHolderText(self.add_test_data_frame, quantity_entry, "Quantity")

        price_label = ctk.CTkLabel(self.add_test_data_frame, text="Price:")
        price_label.place(x=20, y=100)
        price_entry = ctk.CTkEntry(self.add_test_data_frame, width=200)
        price_entry.place(x=150, y=100)
        MyCustomFunctions.EntryPlaceHolderText(self.add_test_data_frame, price_entry, "Price")

        date_label = ctk.CTkLabel(self.add_test_data_frame, text="Date:")
        date_label.place(x=20, y=140)
        date_entry = DateEntry(self.add_test_data_frame, width=12, borderwidth=2)
        date_entry.place(x=190, y=180)

        type_label = ctk.CTkLabel(self.add_test_data_frame, text="Type:")
        type_label.place(x=20, y=180)
        type_options = [
            "Rent", "Utilities", "Salaries", "Insurance", "Equipment", "Supplies",
            "Marketing", "Services", "Training", "Travel", "Food", "Other"
        ]
        type_option_menu = ctk.CTkOptionMenu(self.add_test_data_frame, values=type_options)
        type_option_menu.set("Type:")
        type_option_menu.place(x=150, y=180)

        user_label = ctk.CTkLabel(self.add_test_data_frame, text="User:")
        user_label.place(x=20, y=220)
        user_entry = ctk.CTkEntry(self.add_test_data_frame, width=200)
        MyCustomFunctions.EntryPlaceHolderText(self.add_test_data_frame, user_entry, self.current_user)
        user_entry.configure(state="disabled")
        user_entry.place(x=150, y=220)

        # Buttons
        back_button = ctk.CTkButton(
            self.add_test_data_frame,
            text="Back",
            command=lambda: (self.add_test_data_window.withdraw(), self.show_main_window(self.add_test_data_window)),
            width=140
        )
        back_button.place(x=50, y=260)

        submit_button = ctk.CTkButton(
            self.add_test_data_frame,
            text="Submit",
            width=140,
            command=lambda: (self.add_test_data_window.withdraw(), self.submit_expense_db([name_entry.get(),
                            quantity_entry.get(), price_entry.get(), type_option_menu.get(), datetime.strptime(
                            date_entry.get(), "%m/%d/%y").strftime('%Y-%m-%d')], [f"{
            self.main_db.return_total_expense_amount() + 1:06d}", self.current_user, name_entry.get(),
            quantity_entry.get(), price_entry.get(), type_option_menu.get(), datetime.strptime(date_entry.get(),
            "%m/%d/%y").strftime('%Y-%m-%d')], self.add_test_data_window)))
        submit_button.place(x=200, y=260)

        self.add_test_data_window.mainloop()

    def import_data(self):
        try:
            self.remove_main_window()
            # Create the import window
            import_window = ctk.CTk()
            import_window.title("Import Data")
            import_window.geometry("400x200+760+200")
            import_window.resizable(False, False)

            # Define callback to select a file
            def select_file(selection):
                file_path = filedialog.askopenfilename(
                    title="Select an Excel File",
                    filetypes=[("Excel Files", "*.xlsx *.xls")]
                )
                if not file_path:
                    MyMessageBoxes.ShowMessage().show_info("No file selected.")
                    return

                try:
                    # Load data from the selected file
                    data = pd.read_excel(file_path)

                    # Ensure required columns exist based on the selection
                    if selection == "Users":
                        required_columns = {"UserID", "FirstName", "LastName", "Email", "PhoneNumber", "HashedPassword",
                                            "Level", "Salary"}
                    elif selection == "Expenses":
                        required_columns = {"ExpenseID", "UserID", "Quantity", "Price", "Type", "Date"}
                    else:
                        MyMessageBoxes.ShowMessage().show_error("Invalid selection.")
                        return

                    if not required_columns.issubset(data.columns):
                        MyMessageBoxes.ShowMessage().show_error(
                            f"Missing required columns for {selection}: {required_columns - set(data.columns)}"
                        )
                        return

                    # Call the database function
                    self.main_db.insert_data_into_database(data, selection_menu.get(), lambda: (
                        import_window.withdraw(), self.show_main_window()))
                except Exception as error:
                    MyMessageBoxes.ShowMessage().show_error(f"Error processing file: {error}")

            # Option menu for selecting Users or Expenses
            selection_label = ctk.CTkLabel(import_window, text="Select Data Type to Import:")
            selection_label.pack(pady=(20, 10))

            options = ["Users", "Expenses"]
            selection_menu = ctk.CTkOptionMenu(import_window, values=options)
            selection_menu.pack(pady=(0, 20))

            # Import button to handle file selection and processing
            import_button = ctk.CTkButton(
                import_window,
                text="Import",
                command=lambda: select_file(selection_menu.get()),
            )
            import_button.pack(pady=10, padx=10, side='right')

            # Back button to return to the main window
            back_button = ctk.CTkButton(
                import_window,
                text="Back",
                command=lambda: (import_window.withdraw(), self.show_main_window()),
            )
            back_button.pack(pady=10, padx=10, side='left')
            import_window.mainloop()

        except Exception as e:
            MyMessageBoxes.ShowMessage().show_error(f"An error occurred in the import process: {e}")

    def wipe_database(self):
        self.remove_main_window()
        wipe_db_window = ctk.CTkToplevel()
        wipe_db_window.title("Wipe Database")
        wipe_db_window.geometry("400x200+760+200")
        wipe_db_window.resizable(False, False)
        db_frame = ctk.CTkFrame(wipe_db_window)
        db_frame.pack(expand=True, fill='both')
        wipe_db_label = ctk.CTkLabel(db_frame, text="Enter your password below to wipe the database:", font=(
            "Arial", 14))
        wipe_db_label.pack(pady=10, fill='both')
        db_password_entry = ctk.CTkEntry(db_frame)
        MyCustomFunctions.EntryPlaceHolderText(db_frame, db_password_entry, "Password:")
        MyCustomFunctions.ShowHidePasswordText(db_password_entry)
        MyCustomFunctions.ShowHidePasswordWidget(db_frame, db_password_entry, 0.73, 0.4)
        db_password_entry.place(relx=0.5, rely=0.4, anchor='center')
        back_button = ctk.CTkButton(db_frame, text="Back", command=lambda: (wipe_db_window.withdraw(),
                                                                            self.show_main_window()))
        back_button.place(relx=0.2, rely=0.9, anchor='center')
        wipe_db_button = ctk.CTkButton(db_frame, text="Wipe Database", command=lambda: self.try_wipe_db(
            self.current_user, db_password_entry.get(), wipe_db_window))
        wipe_db_button.place(relx=0.8, rely=0.9, anchor='center')

    def try_wipe_db(self, current_user, given_password, show_hide_window):
        try:
            if PasswordHasher.Hasher().verify_password(self.main_db.return_user_hashed_password(current_user),
                                                       given_password):
                show_hide_window.withdraw()
                confirm_dp_wipe = MyMessageBoxes.ShowMessage().ask_question("Are you sure you want to wipe the"
                                                                            " database?", "Yes", "No",
                                                                            "Back", "Back")
                if confirm_dp_wipe == "Back":
                    show_hide_window.deiconify()
                elif confirm_dp_wipe == "No":
                    self.show_main_window()
                elif confirm_dp_wipe == "Yes":
                    MyDatabase.DisplayExcelSpreadsheet(self.current_user, ctk.CTk()).download_expenses()
                    MyDatabase.DisplayExcelSpreadsheet(self.current_user, ctk.CTk(),
                                                       show_users=True).download_expenses()
                    MyMessageBoxes.ShowMessage().show_info(f"Downloaded current database, wiping now.")
                    self.main_db.wipe_database()
                    self.show_main_window()
        except Exception as e:
            return e


if __name__ == '__main__':
    ctk.set_appearance_mode("light")

    root = ctk.CTk()
    root.title("Expense Tracker")
    root.geometry('850x525+425+175')
    root.resizable(False, False)
    account_frame = (AdminWindow
                     (root, "CM0000"))
    root.mainloop()
