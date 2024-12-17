import mysql.connector
import customtkinter as ctk
from tkinter import ttk
from openpyxl import Workbook
from openpyxl.styles import Alignment
from pathlib import Path
from datetime import datetime
import MyMessageBoxes


class AccountsDatabase:
    def __init__(self):
        try:
            self.main_db = mysql.connector.connect(
                host='127.0.0.1',
                user='admin',
                password='rcV])R%tN3YnS"b'
            )
            self.create_tables()
        except mysql.connector.errors.ProgrammingError as e:
            self.bad_connection(e)

    def create_tables(self):
        db_cursor = self.main_db.cursor()
        # Ensure schema exists and is in use
        db_cursor.execute("CREATE SCHEMA IF NOT EXISTS ExpenseDatabase")
        db_cursor.execute("USE ExpenseDatabase")

        # Table 1: UserTable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserTable (
                UserID VARCHAR(6) PRIMARY KEY,
                FirstName CHAR(30) NOT NULL,
                LastName CHAR(30) NOT NULL,
                Email VARCHAR(256) NOT NULL,
                PhoneNumber CHAR(11) NOT NULL,
                HashedPassword CHAR(76) NOT NULL
            )
        """)

        # Table 2: SalaryTable with One-to-One relationship with UserTable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS SalaryTable (
                UserID VARCHAR(6),
                Level INT NOT NULL,
                Salary INT NOT NULL,
                PRIMARY KEY (UserID, Level),
                FOREIGN KEY (UserID) REFERENCES UserTable(UserID) ON DELETE CASCADE
            )
        """)

        # Table 3: ExpenseTable with One-to-Many relationship with UserTable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS ExpenseTable (
                ExpenseID VARCHAR(6) PRIMARY KEY,
                UserID VARCHAR(6),
                Name VARCHAR(30) NOT NULL,
                Quantity INT NOT NULL,
                Price DECIMAL(10, 2) NOT NULL,
                Type VARCHAR(30) NOT NULL,
                Date DATE NOT NULL,
                FOREIGN KEY (UserID) REFERENCES UserTable(UserID) ON DELETE CASCADE
            )
        """)

        db_cursor.close()
        self.main_db.database = "ExpenseDatabase"

    @staticmethod
    def bad_connection(given_error):
        return given_error

    def submit_expense_db(self, expense_inputs):
        try:
            cursor = self.main_db.cursor()  # Assuming `self.main_db` is the database connection
            query = """
                    INSERT INTO ExpenseTable (ExpenseID, UserID, Name, Quantity, Price, Type, Date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, expense_inputs)
            self.main_db.commit()
            cursor.close()
        except Exception as error:
            raise error

    def add_user_to_db(self, user_id, first_name, last_name, email, phone_number, hashed_password, level, salary):
        try:
            cursor = self.main_db.cursor()

            first_query = """
                       INSERT INTO UserTable (UserID, FirstName, LastName, Email, PhoneNumber, HashedPassword)
                       VALUES (%s, %s, %s, %s, %s, %s)
                   """
            cursor.execute(first_query, (user_id, first_name, last_name, email, phone_number, hashed_password))

            second_query = """
                        INSERT INTO SalaryTable (UserID, Level, Salary) 
                        VALUES (%s, %s, %s)
            """
            cursor.execute(second_query, (user_id, level, salary))

            self.main_db.commit()  # Commit changes to the database
            cursor.close()
            return
        except Exception as given_error:
            print(given_error)

    def check_user_level(self, given_userid):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT LEVEL FROM SalaryTable WHERE UserID = %s",
                              (given_userid,))
            user_level = db_cursor.fetchone()[0]
            return user_level
        except Exception as given_error:
            return given_error

    def check_user_exists(self, given_userid):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT HashedPassword FROM UserTable WHERE UserID = %s",
                              (given_userid,))
            hashed_pass_from_user = db_cursor.fetchone()[0]
            return hashed_pass_from_user
        except mysql.connector.errors.InternalError:
            return False
        except TypeError:
            return False

    def return_total_expense_amount(self):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT COUNT(*) FROM ExpenseTable")
            count = db_cursor.fetchone()[0]
            db_cursor.close()
            return count
        except Exception as given_error:
            return given_error

    def return_account_amount(self):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT COUNT(*) FROM UserTable")
            count = db_cursor.fetchone()[0]  # Fetch the first element from the result tuple
            db_cursor.close()
            self.main_db.close()
            return count
        except Exception as error:
            return error

    def return_expenses_from_user(self, current_user):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            cursor.execute("""
                SELECT ExpenseID, Type, Quantity, Price, Date 
                FROM ExpenseTable 
                WHERE UserID = %s
            """, (current_user,))
            expenses = cursor.fetchall()
            self.main_db.commit()
            cursor.close()
            return expenses
        except Exception as given_error:
            return given_error

    def return_total_inputted_from_user(self, current_user):
        try:
            cursor = self.main_db.cursor()
            query = """
                SELECT COUNT(*) AS total_expenses
                FROM ExpenseTable
                WHERE UserID = %s;
            """
            cursor.execute(query, (current_user,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Exception as error:
            return error

    def return_expenses_summed(self, current_user):
        expenses_from_user = self.return_expenses_from_user(current_user)
        total_sum = sum(expense["Price"] * expense["Quantity"] for expense in expenses_from_user)
        return total_sum

    def get_expenses_by_type(self, current_user):
        """
        Retrieves the total expense amount for each type for the given user.

        Args:
            current_user (str): The user ID whose expenses need to be retrieved.

        Returns:
            dict: A dictionary where keys are expense types and values are the summed amounts.
        """
        try:
            cursor = self.main_db.cursor(dictionary=True)
            query = """
                SELECT Type, SUM(Price * Quantity) AS TotalAmount
                FROM ExpenseTable
                WHERE UserID = %s
                GROUP BY Type;
            """
            cursor.execute(query, (current_user,))
            results = cursor.fetchall()
            cursor.close()

            # Convert the query results into a dictionary
            expenses_by_type = {row['Type']: row['TotalAmount'] for row in results}
            return expenses_by_type
        except Exception as error:
            raise error

    def remove_given_expenses(self, given_expense_ids):
        """Deletes expenses with the given expense_ids from the ExpenseTable."""
        try:
            cursor = self.main_db.cursor()

            # Create the SQL DELETE query with placeholders
            query = "DELETE FROM ExpenseTable WHERE ExpenseID IN (%s)"

            # Generate a string of placeholders for each expense_id
            format_strings = ','.join(['%s'] * len(given_expense_ids))

            # Execute the query with the expense_id list as the parameters
            cursor.execute(query % format_strings, tuple(given_expense_ids))

            # Commit the transaction
            self.main_db.commit()
            cursor.close()

            # Check how many rows were deleted
            if cursor.rowcount > 0:
                return f"Successfully deleted {cursor.rowcount} expense(s)."
            else:
                raise "No expenses found with the given IDs."

        except Exception as e:
            raise f"Error occurred while removing expenses: {e}"


class ExpenseViewer:
    def __init__(self, user_id, parent, submit_frame):
        self.spreadsheet_frame = ctk.CTkFrame(parent)
        self.spreadsheet_frame.pack(expand=True, fill='both')
        self.db = AccountsDatabase()
        self.user_id = user_id
        self.expenses = self.db.return_expenses_from_user(self.user_id)
        if self.expenses:

            # Scrollable frame for spreadsheet-like display
            self.scrollable_frame = ctk.CTkScrollableFrame(self.spreadsheet_frame, width=580, height=300)
            self.scrollable_frame.pack(fill="both", expand=True)

            # Column headers
            headers = ["Select", "ExpenseID", "Quantity", "Price", "Date"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 14, "bold"))
                label.grid(row=0, column=col, padx=10, pady=5)

            # Display expenses with checkboxes
            self.expense_checkboxes = []
            self.display_expenses()

            # Submit button to handle selected expenses
            self.submit_button = ctk.CTkButton(submit_frame, text="Submit",
                                               command=self.get_selected_expenses)
            self.submit_button.place(x=315, y=250)
        else:
            ctk.CTkLabel(self.spreadsheet_frame, text="No expenses found from your user.\n Only admins can see all "
                                                      "expenses.").place(x=100, y=100)

    def display_expenses(self):
        for row, expense in enumerate(self.expenses, start=1):
            # Checkbox for each expense
            checkbox_var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.scrollable_frame, variable=checkbox_var, text="")
            checkbox.grid(row=row, column=0, padx=10, pady=5)
            self.expense_checkboxes.append((checkbox_var, expense["ExpenseID"]))

            # Labels for each data column
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["ExpenseID"])).grid(row=row, column=1, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["Quantity"])).grid(row=row, column=2, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=f"${expense['Price']:.2f}").grid(row=row, column=3, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["Date"])).grid(row=row, column=4, padx=10)

    def get_selected_expenses(self):
        selected_expenses = [expense_id for var, expense_id in self.expense_checkboxes if var.get()]
        try:
            remove_expenses = AccountsDatabase().remove_given_expenses(selected_expenses)
            MyMessageBoxes.ShowMessage().show_info(remove_expenses)
        except Exception as given_error:
            MyMessageBoxes.ShowMessage().show_error(given_error)


class ExpenseExcelSpreadsheet:
    def __init__(self, user_id, parent):
        self.parent = parent
        self.db = AccountsDatabase()
        self.user_id = user_id
        self.expenses = self.db.return_expenses_from_user(self.user_id)

        # Frame for the Treeview display
        self.excel_spreadsheet_frame = ctk.CTkFrame(self.parent)
        self.excel_spreadsheet_frame.pack(fill="both", expand=True)

        if self.expenses:
            # Treeview setup for displaying expenses
            self.tree = ttk.Treeview(self.excel_spreadsheet_frame, columns=("ExpenseID", "Quantity", "Price",
                                                                            "Type", "Date"),
                                     show="headings")
            self.tree.heading("ExpenseID", text="ExpenseID")
            self.tree.heading("Quantity", text="Quantity")
            self.tree.heading("Price", text="Price")
            self.tree.heading("Type", text="Type")
            self.tree.heading("Date", text="Date")
            self.tree.pack(side="left", fill="both", expand=True)

            # Load expenses data for display
            self.display_expenses()
        else:
            ctk.CTkLabel(self.excel_spreadsheet_frame, text="No expenses found from your user.\n Only admins can see"
                                                            " all expenses.").place(x=100, y=100)

    def display_expenses(self):
        # Get user expenses using the database method

        # Populate Treeview with the data
        for expense in self.expenses:
            if isinstance(expense, dict):  # Ensure each row is a dictionary
                self.tree.insert(
                    "", "end",
                    values=(
                        expense.get("ExpenseID", ""),
                        expense.get("Type", "Unknown"),  # Use 'Unknown' if Type is missing
                        expense.get("Quantity", 0),
                        f"£{expense.get('Price', 0):.2f}",
                        expense.get("Date", ""),
                    ),
                )

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.excel_spreadsheet_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def download_expenses(self):
        if self.expenses:
            workbook = Workbook()
            sheet = workbook.active
            sheet.column_dimensions['A'].width = 10
            sheet.column_dimensions['B'].width = 10
            sheet.column_dimensions['C'].width = 10
            sheet.column_dimensions['D'].width = 10
            sheet.column_dimensions['E'].width = 15
            sheet.title = "User Expenses"

            # Define the headers and write them to the first row
            headers = ["ExpenseID", "Quantity", "Price", "Type", "Date"]
            sheet.append(headers)

            # Add expense data rows to the sheet
            for expense in self.expenses:
                sheet.append([expense["ExpenseID"], expense["Quantity"], expense["Price"],
                              expense["Type"], expense["Date"]])

            # Determine the path to the Downloads folder
            downloads_path = Path.home() / "Downloads"
            # Name the file with a timestamp for uniqueness
            filename = f"expenses_{self.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = downloads_path / filename
            # Save the workbook
            workbook.save(file_path)
        else:
            raise Exception("No expenses found from your user.")


if __name__ == '__main__':
    AccountsDatabase()
