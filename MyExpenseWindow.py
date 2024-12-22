import customtkinter as ctk
from PIL import Image
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import MyMessageBoxes
import MyCustomFunctions
import MyDatabase
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.dates as mdates


class DefaultWindow:
    def __init__(self, parent, current_user):
        self.parent = parent
        self.current_user = current_user
        self.main_db = MyDatabase.AccountsDatabase()
        self.root = ctk.CTkFrame(parent)
        self.root.pack(expand=True, fill="both")

        self.nb = ctk.CTkTabview(self.root, width=500, height=400)
        self.nb.pack(expand=True, fill="both")

        self.setup_notebook()

    def setup_notebook(self):
        self.nb.add("Tracker Settings")
        self.nb.add("Expenses")
        self.nb.add("Graphs")
        self.nb.add("Table")
        self.nb.add("Predictor")
        self.nb.set("Expenses")

        self.setup_expense_window()

    def setup_expense_window(self):
        self.create_tracker_settings_tab()
        self.create_expenses_tab()
        self.create_graphs_tab()
        self.create_table_tab()
        self.create_predictor_tab()

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
        total_expenses_from_user = self.main_db.return_total_inputted_from_user(self.current_user)
        total_expenses_summed = self.main_db.return_expenses_summed(self.current_user)
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
                                                    width=200, height=100, text="Remove Expense(s)", compound="bottom",
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
                                      width=140, command=self.submit_expense_db)
        submit_button.place(x=200, y=240)

        self.add_expense_window.mainloop()

    def submit_expense_db(self):
        inputs = [self.name_entry.get(), self.quantity_entry.get(), self.price_entry.get(),
                  self.type_option_menu.get()]
        placeholders = ["Name", "Quantity", "Price", "Type:"]
        invalid_fields = [placeholder for placeholder, value in zip(placeholders, inputs) if
                          not value.strip() or value == placeholder]
        if invalid_fields:
            MyMessageBoxes.ShowMessage().show_error(
                f"Ensure the following fields are filled correctly:\n{', '.join(invalid_fields)}.")
            return
        inputs = [f"{MyDatabase.AccountsDatabase().return_total_expense_amount() + 1:06d}", self.current_user,
                  self.name_entry.get(), self.quantity_entry.get(), self.price_entry.get(),
                  self.type_option_menu.get(), datetime.now().strftime('%Y-%m-%d')]
        try:
            self.main_db.submit_expense_db(inputs)
            MyMessageBoxes.ShowMessage().show_info("Expense added successfully.")
        except Exception as error:
            MyMessageBoxes.ShowMessage().show_error(f"An error occurred: {error}")

    def remove_expense(self):
        # Create a new CTk window
        self.remove_main_window()
        self.remove_expense_window = ctk.CTk()  # Or ctk.CTkToplevel(self.parent) to make it a child of the main window
        self.remove_expense_frame = ctk.CTkFrame(self.remove_expense_window)
        self.remove_expense_frame.pack(expand=True, fill="both")
        self.remove_expense_window.title("Remove Expense(s)")
        self.remove_expense_window.geometry("600x370+660+200")  # Customize the size

        # Pass the callback function (show_main_window) to ExpenseViewer
        self.expense_spreadsheet = MyDatabase.ExpenseViewer(self.current_user, self.remove_expense_frame,
                                                            self.remove_expense_frame,
                                                            lambda: self.show_main_window(self.remove_expense_window))

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
                                                                 "Cancel", "All years",
                                                                 "Previous year")
        if download_table == "All years":
            try:
                MyDatabase.ExpenseExcelSpreadsheet(self.current_user, ctk.CTk()).download_expenses()
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
        elif download_table == "Cancel":
            self.show_main_window(ctk.CTkToplevel())

    def download_expenses_for_year(self, year, parent):
        try:
            MyDatabase.ExpenseExcelSpreadsheet(self.current_user, ctk.CTk(), year).download_expenses()
            MyMessageBoxes.ShowMessage.show_info(f"Spreadsheet for {year} downloaded successfully.")
            self.show_main_window(parent)
        except Exception as error:
            MyMessageBoxes.ShowMessage.show_info(f"Something went wrong: {str(error)}")

    def create_income_tab(self):
        pass

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
        choose_year_button = ctk.CTkOptionMenu(button_frame, values=[f'Year: {starting_year}',
                                                                     f'Year: {starting_year + 1}',
                                                                     f'Year: {starting_year + 2}'],
                                               variable=current_year)
        choose_year_button.set('Year: 2024')
        choose_year_button.pack(side="left", padx=6, expand=True, fill='both')

        refresh_graph_button = ctk.CTkButton(button_frame, text="Refresh Graph",
                                             command=refresh_graphs)
        refresh_graph_button.pack(side="left", padx=6, expand=True, fill='both')

        # Default graph display
        plot_expenses_over_time()

    def create_table_tab(self):
        """
        Creates the 'Table' tab in the notebook to display an Excel-like, scrollable table for the current user's data,
        including the expense type.
        """
        # Create the Table tab and its main frame
        table_tab = self.nb.tab("Table")
        table_tab_frame = ctk.CTkFrame(table_tab)
        control_frame = ctk.CTkFrame(table_tab_frame)

        # Create a frame for table controls (e.g., refresh button)
        table_tab_frame.pack(fill="both", expand=True)
        control_frame.pack(fill="x", pady=10)

        # Create a frame for the table and scrollbars
        table_frame = ctk.CTkFrame(table_tab_frame)
        table_frame.pack(fill="both", expand=True)

        # Add vertical and horizontal scrollbars
        scrollbar_y = tk.Scrollbar(table_frame, orient="vertical")
        scrollbar_x = tk.Scrollbar(table_frame, orient="horizontal")

        # Create the Treeview widget for displaying the table
        tree = ttk.Treeview(
            table_frame,
            columns=("ExpenseID", "Type", "Quantity", "Price", "Date"),
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
        headers = ["ExpenseID", "Type", "Quantity", "Price", "Date"]
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        def fetch_table_data():
            """
            Fetches data from the database and populates the table.
            """
            # Clear the table
            tree.delete(*tree.get_children())

            try:
                # Retrieve data from the database
                expenses = self.main_db.return_expenses_from_user(self.current_user)

                if not expenses:
                    raise ValueError("No data available to display.")

                # Insert rows into the Treeview
                for row in expenses:
                    if isinstance(row, dict):  # Ensure each row is a dictionary
                        tree.insert(
                            "", "end",
                            values=(
                                row.get("ExpenseID", ""),
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

        current_user_label = ctk.CTkLabel(control_frame, text=f"User {self.current_user}'s Expenses:")
        current_user_label.pack(side="bottom", expand=True)
        # Add Refresh Button to control frame
        refresh_button = ctk.CTkButton(control_frame, text="Refresh Table", command=refresh_table)
        refresh_button.pack(side="top", expand=True)

        # Fetch and display data initially
        fetch_table_data()

    def create_predictor_tab(self):
        """
        Creates the 'Plotter' tab in the notebook to predict future expenses using historical data and display them on a graph.
        """

        # Create the Plotter tab and its main frame
        plotter_tab = self.nb.tab("Predictor")
        plotter_tab_frame = ctk.CTkFrame(plotter_tab)
        plotter_tab_frame.pack(fill="both", expand=True)

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
        predict_button = ctk.CTkButton(
            plotter_tab_frame,
            text="Refresh Future Expenses Prediction",
            command=fetch_and_predict_expenses
        )
        predict_button.pack(pady=10)

        # Display the initial empty graph
        fetch_and_predict_expenses()


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
    account_frame = (DefaultWindow
                     (root, "CM0000"))
    root.mainloop()
