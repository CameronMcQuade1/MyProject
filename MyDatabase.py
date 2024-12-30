import mysql.connector
import customtkinter as ctk
from tkinter import ttk
from openpyxl import Workbook
from pathlib import Path
from datetime import datetime
import MyMessageBoxes


class AccountsDatabase:
    def __init__(self):
        try:
            self.main_db = mysql.connector.connect(
                host='db4free.net',
                database='expensedatabase',
                username='expensedatabase',
                password='&FNBra!4117LVv'
            )
            self.create_tables()
        except mysql.connector.errors.ProgrammingError as e:
            self.bad_connection(e)

    def create_tables(self):
        db_cursor = self.main_db.cursor()
        # Ensure schema exists and is in use
        db_cursor.execute("CREATE SCHEMA IF NOT EXISTS ExpenseDatabase")
        db_cursor.execute("USE ExpenseDatabase")

        # Table 1: usertable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS usertable (
                UserID VARCHAR(6) PRIMARY KEY,
                FirstName CHAR(30) NOT NULL,
                LastName CHAR(30) NOT NULL,
                Email VARCHAR(256) NOT NULL,
                PhoneNumber CHAR(11) NOT NULL,
                HashedPassword CHAR(76) NOT NULL
            )
        """)

        # Table 2: salarytable with One-to-One relationship with usertable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS salarytable (
                UserID VARCHAR(6),
                Level INT NOT NULL,
                Salary INT NOT NULL,
                PRIMARY KEY (UserID, Level),
                FOREIGN KEY (UserID) REFERENCES usertable(UserID) ON DELETE CASCADE
            )
        """)

        # Table 3: expensetable with One-to-Many relationship with usertable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS expensetable (
                ExpenseID VARCHAR(6) PRIMARY KEY,
                UserID VARCHAR(6),
                Name VARCHAR(30) NOT NULL,
                Quantity INT NOT NULL,
                Price DECIMAL(10, 2) NOT NULL,
                Type VARCHAR(30) NOT NULL,
                Date DATE NOT NULL,
                FOREIGN KEY (UserID) REFERENCES usertable(UserID) ON DELETE CASCADE
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
                    INSERT INTO expensetable (ExpenseID, UserID, Name, Quantity, Price, Type, Date)
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
                       INSERT INTO usertable (UserID, FirstName, LastName, Email, PhoneNumber, HashedPassword)
                       VALUES (%s, %s, %s, %s, %s, %s)
                   """
            cursor.execute(first_query, (user_id, first_name, last_name, email, phone_number, hashed_password))

            second_query = """
                        INSERT INTO salarytable (UserID, Level, Salary) 
                        VALUES (%s, %s, %s)
            """
            cursor.execute(second_query, (user_id, level, salary))

            self.main_db.commit()  # Commit changes to the database
            cursor.close()
            return
        except Exception as given_error:
            return given_error

    def check_user_level(self, given_userid):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT LEVEL FROM salarytable WHERE UserID = %s",
                              (given_userid,))
            user_level = db_cursor.fetchone()[0]
            return user_level
        except Exception as given_error:
            return given_error

    def check_user_exists(self, given_userid):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT HashedPassword FROM usertable WHERE UserID = %s",
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
            db_cursor.execute("SELECT COUNT(*) FROM expensetable")
            count = db_cursor.fetchone()[0]
            db_cursor.close()
            return count
        except Exception as given_error:
            return given_error

    def return_account_amount(self):
        try:
            db_cursor = self.main_db.cursor()
            db_cursor.execute("SELECT COUNT(*) FROM usertable")
            count = db_cursor.fetchone()[0]  # Fetch the first element from the result tuple
            db_cursor.close()
            self.main_db.close()
            return count
        except Exception as error:
            return error

    def return_expenses_from_user(self, current_user):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            if self.check_user_level(current_user) == 0:
                cursor.execute("""
                    SELECT ExpenseID, UserID, Type, Quantity, Price, Date 
                    FROM expensetable 
                    WHERE UserID = %s
                """, (current_user,))
            else:
                cursor.execute("""
                                    SELECT ExpenseID, UserID, Type, Quantity, Price, Date 
                                    FROM expensetable 
                                """)
            expenses = cursor.fetchall()
            self.main_db.commit()
            cursor.close()
            return expenses
        except Exception as given_error:
            return given_error

    def return_total_inputted_from_user(self, current_user):
        try:
            cursor = self.main_db.cursor()
            if self.check_user_level(current_user) == 0:
                query = """
                    SELECT COUNT(*) AS total_expenses
                    FROM expensetable
                    WHERE UserID = %s;
                """
                cursor.execute(query, (current_user,))
            else:
                query = """
                    SELECT COUNT(*) AS total_expenses
                    FROM expensetable
                """
                cursor.execute(query)
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
            if self.check_user_level(current_user) == 0:
                query = """
                    SELECT Date, Type, SUM(Price * Quantity) AS TotalAmount
                    FROM expensetable
                    WHERE UserID = %s
                    GROUP BY Date, Type;
                """
                cursor.execute(query, (current_user,))
            else:
                query = """
                                    SELECT Date, Type, SUM(Price * Quantity) AS TotalAmount
                                    FROM expensetable
                                    GROUP BY Date, Type;
                                """
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Convert the query results into a dictionary
            return results
        except Exception as error:
            raise error

    def remove_given_expenses(self, given_expense_ids):
        """Deletes expenses with the given expense_ids from the expensetable."""
        try:
            cursor = self.main_db.cursor()

            # Create the SQL DELETE query with placeholders
            query = "DELETE FROM expensetable WHERE ExpenseID IN (%s)"

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

    def return_all_users(self):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            query = """
                    SELECT usertable.UserID, FirstName, LastName, Email, PhoneNumber, Level, Salary
                    FROM usertable, salarytable
                    WHERE salarytable.UserID = usertable.UserID
                """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as given_error:
            return given_error

    def return_all_expenses(self):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            query = """
                    SELECT ExpenseID, UserID, Name, Quantity, Price, Type, Date
                    FROM expensetable
                """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as given_error:
            return given_error

    def remove_given_users(self, given_user_ids):
        try:
            cursor = self.main_db.cursor()
            format_strings = ','.join(['%s'] * len(given_user_ids))
            query1 = f"DELETE FROM usertable WHERE UserID IN ({format_strings})"
            cursor.execute(query1, tuple(given_user_ids))
            query2 = f"DELETE FROM salarytable WHERE UserID IN ({format_strings})"
            cursor.execute(query2, tuple(given_user_ids))
            self.main_db.commit()
            cursor.close()
            return f"Successfully deleted {len(given_user_ids)} User ID(s)."
        except Exception as e:
            return f"Error occurred while removing users: {e}"


class ExpenseViewer:
    def __init__(self, user_id, parent, submit_frame, on_remove_callback, show_users=None):
        self.__parent = parent
        self.spreadsheet_frame = ctk.CTkFrame(parent)
        self.spreadsheet_frame.pack(expand=True, fill='both')
        self.db = AccountsDatabase()
        self.user_id = user_id
        self.show_users = show_users if show_users else None
        if self.show_users:
            self.information = self.db.return_all_users()
        elif not self.show_users and self.db.check_user_level(user_id) == 0:
            self.information = self.db.return_expenses_from_user(self.user_id)
        else:
            self.information = self.db.return_all_expenses()

        # Store the callback function
        self.on_remove_callback = on_remove_callback

        if self.information:
            # Scrollable frame for spreadsheet-like display
            self.scrollable_frame = ctk.CTkScrollableFrame(self.spreadsheet_frame, width=580, height=300)
            self.scrollable_frame.pack(fill="both", expand=True)

            # Column headers
            if self.show_users:
                headers = ["Select", "UserID", "FirstName", "LastName", "Email", "PhoneNumber", "Level", "Salary"]
            elif not self.show_users and self.db.check_user_level(self.user_id) == 0:
                headers = ["Select", "ExpenseID", "Quantity", "Price", "Date"]
            else:
                headers = ["Select", "ExpenseID", "UserID", "Quantity", "Price", "Type", "Date"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 14, "bold"))
                label.grid(row=0, column=col, padx=10, pady=5)

            # Display expenses with checkboxes
            self.information_checkboxes = []
            self.display_information()

            # Submit button to handle selected expenses
            self.submit_button = ctk.CTkButton(submit_frame, text="Submit",
                                               command=self.get_selected_information)
            self.submit_button.pack(expand=True, side='right')
        else:
            ctk.CTkLabel(self.spreadsheet_frame, text="No expenses found from your user.\n Only admins can see all "
                                                      "expenses.").place(x=100, y=100)

    def display_information(self):
        for row, info in enumerate(self.information, start=1):
            # Checkbox for each expense
            checkbox_var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.scrollable_frame, variable=checkbox_var, text="", width=30)
            checkbox.grid(row=row, column=0, padx=10, pady=5)
            if not self.show_users and self.db.check_user_level(self.user_id) == 0:
                self.information_checkboxes.append((checkbox_var, info["ExpenseID"]))

                # Labels for each data column
                ctk.CTkLabel(self.scrollable_frame, text=str(info["ExpenseID"])).grid(row=row, column=1, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Quantity"])).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=f"${info['Price']:.2f}").grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Date"])).grid(row=row, column=4, padx=10)
            elif not self.show_users and self.db.check_user_level(self.user_id) == 1:
                self.information_checkboxes.append((checkbox_var, info["ExpenseID"]))

                # Labels for each data column
                ctk.CTkLabel(self.scrollable_frame, text=str(info["ExpenseID"])).grid(row=row, column=1, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["UserID"])).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Quantity"])).grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=f"${info['Price']:.2f}").grid(row=row, column=4, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Type"])).grid(row=row, column=5, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Date"])).grid(row=row, column=6, padx=10)
            else:
                self.information_checkboxes.append((checkbox_var, info["UserID"]))

                # Labels for each data column
                ctk.CTkLabel(self.scrollable_frame, text=str(info["UserID"])).grid(row=row, column=1, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["FirstName"])).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info['LastName'])).grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info['Email'])).grid(row=row, column=4, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info['PhoneNumber'])).grid(row=row, column=5, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Level"])).grid(row=row, column=6, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Salary"])).grid(row=row, column=7, padx=10)

    def get_selected_information(self):
        try:
            if self.show_users:
                selected_information = [user_id for var, user_id in self.information_checkboxes if var.get()]
            else:
                selected_information = [expense_id for var, expense_id in self.information_checkboxes if var.get()]
                # Attempt to remove the selected expenses from the database
            remove_expenses = AccountsDatabase().remove_given_expenses(selected_information) if not (
                self.show_users) else AccountsDatabase().remove_given_users(selected_information)
            MyMessageBoxes.ShowMessage().show_info(remove_expenses)

            self.on_remove_callback()

        except Exception as given_error:
            MyMessageBoxes.ShowMessage().show_error(given_error)


class DisplayExcelSpreadsheet:
    def __init__(self, user_id, parent, year=None, show_users=None):
        self.parent = parent
        self.db = AccountsDatabase()
        self.user_id = user_id
        self.year = year
        self.show_users = show_users if show_users else None
        self.information = self.get_information()  # Fetch expenses based on the year filter

        # Frame for the Treeview display
        self.excel_spreadsheet_frame = ctk.CTkFrame(self.parent)
        self.excel_spreadsheet_frame.pack(fill="both", expand=True)

        if self.information:
            # Treeview setup for displaying expenses
            if not show_users:
                self.tree = ttk.Treeview(
                    self.excel_spreadsheet_frame,
                    columns=("ExpenseID", "UserID", "Quantity", "Price", "Type", "Date"),
                    show="headings",
                )
                # Define headings and center-align text below
                headings = [("ExpenseID", 30), ("UserID", 30), ("Quantity", 70), ("Price", 60), ("Type", 50), ("Date", 100)]
                for col, width in headings:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, anchor="center", width=width)  # Center text and set column width

            elif show_users:
                self.tree = ttk.Treeview(
                    self.excel_spreadsheet_frame,
                    columns=("UserID", "FirstName", "LastName", "Email", "Number", "Level", "Salary"),
                    show="headings",
                )
                # Define headings and center-align text below
                headings = [
                    ("UserID", 80),
                    ("FirstName", 100),
                    ("LastName", 100),
                    ("Email", 150),
                    ("Number", 80),
                    ("Level", 60),
                    ("Salary", 100),
                ]
                for col, width in headings:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, anchor="center", width=width)  # Center text and set column width
            self.tree.pack(side="left", fill="both", expand=True)

            # Load expenses data for display
            self.display_expenses()
        else:
            if self.db.check_user_level(self.user_id) == 0:
                ctk.CTkLabel(self.excel_spreadsheet_frame, text="No expenses found for your user.\n Only admins can see"
                                                                " all expenses.").place(x=100, y=100)
            else:
                ctk.CTkLabel(self.excel_spreadsheet_frame, text="No expenses found in the database").place(x=100, y=100)

    def get_information(self):
        """Fetch expenses for the user, optionally filtering by year."""
        if self.show_users:
            all_data = self.db.return_all_users()
        else:
            all_data = self.db.return_expenses_from_user(self.user_id)
        if self.year:
            # Filter expenses by the specified year
            filtered_expenses = [
                expense for expense in all_data
                if datetime.strptime(str(expense['Date']), '%Y-%m-%d').year == self.year
            ]
            return filtered_expenses
        return all_data

    def display_expenses(self):
        """Populate the Treeview with expense data."""
        if not self.show_users:
            for expense in self.information:
                if isinstance(expense, dict):  # Ensure each row is a dictionary
                    self.tree.insert(
                        "", "end",
                        values=(
                            expense.get("ExpenseID", ""),
                            expense.get("UserID", ""),
                            expense.get("Quantity", 0),
                            f"£{expense.get('Price', 0):.2f}",
                            expense.get("Type", "Unknown"),
                            expense.get("Date", ""),
                        ),
                    )
        elif self.show_users:
            for user in self.information:
                if isinstance(user, dict):
                    self.tree.insert(
                        "", "end",
                        values=(
                            user.get("UserID", ""),
                            user.get("FirstName", ""),
                            user.get("LastName", ""),
                            user.get("Email", ""),
                            user.get("PhoneNumber", ""),
                            user.get("Level", ""),
                            user.get("Salary", ""),
                        ),
                    )

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.excel_spreadsheet_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def download_expenses(self):
        """Export the displayed expenses to an Excel spreadsheet."""
        if self.information:
            workbook = Workbook()
            sheet = workbook.active
            sheet.column_dimensions['A'].width = 10
            sheet.column_dimensions['B'].width = 10
            sheet.column_dimensions['C'].width = 10
            sheet.column_dimensions['D'].width = 10
            sheet.column_dimensions['E'].width = 10
            sheet.column_dimensions['F'].width = 15
            if not self.show_users:
                sheet.title = f"User Expenses {self.year if self.year else 'All'}"

                # Define the headers and write them to the first row
                headers = ["ExpenseID", "UserID", "Quantity", "Price", "Type", "Date"]
                sheet.append(headers)

                # Add expense data rows to the sheet
                for expense in self.information:
                    sheet.append([expense["ExpenseID"], expense["UserID"], expense["Quantity"], expense["Price"],
                                  expense["Type"], expense["Date"]])

                # Determine the path to the Downloads folder
                downloads_path = Path.home() / "Downloads"
                # Name the file with a timestamp for uniqueness
                filename = f"expenses_{self.user_id}_{self.year if self.year else 'all'}_{datetime.now().strftime(
                    '%Y%m%d_%H%M%S')}.xlsx"
            elif self.show_users:
                sheet.title = f"User List"

                # Define the headers and write them to the first row
                headers = ["UserID", "FirstName", "LastName", "Email", "PhoneNumber", "Level", "Salary"]
                sheet.append(headers)

                # Add expense data rows to the sheet
                for user in self.information:
                    sheet.append([user["UserID"], user["FirstName"], user["LastName"],
                                  user["Email"], user["PhoneNumber"], user["Level"], user["Salary"]])

                # Determine the path to the Downloads folder
                downloads_path = Path.home() / "Downloads"
                # Name the file with a timestamp for uniqueness
                filename = f"UserList{datetime.now().strftime(
                    '%Y%m%d_%H%M%S')}.xlsx"

            file_path = downloads_path / filename
            # Save the workbook
            workbook.save(file_path)
        else:
            raise Exception("No expenses found for your user from the year chosen.")


if __name__ == '__main__':
    AccountsDatabase().return_all_users()
