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
            self.cursor = self.main_db.cursor()
        #   self.create_tables()
        except mysql.connector.errors.ProgrammingError as e:
            self.bad_connection(e)

    def create_tables(self):
        self.cursor = self.main_db.cursor()
        # Ensure schema exists and is in use
        self.cursor.execute("CREATE SCHEMA IF NOT EXISTS ExpenseDatabase")
        self.cursor.execute("USE ExpenseDatabase")

        # Table 1: usertable
        self.cursor.execute("""
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS salarytable (
                UserID VARCHAR(6),
                Level INT NOT NULL,
                Salary INT NOT NULL,
                PRIMARY KEY (UserID, Level),
                FOREIGN KEY (UserID) REFERENCES usertable(UserID) ON DELETE CASCADE
            )
        """)

        # Table 3: expensetable with One-to-Many relationship with usertable
        self.cursor.execute("""
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

        self.cursor.close()
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

    def return_expenses_from_user(self, current_user=None):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            if self.check_user_level(current_user) == 0:
                cursor.execute("""
                    SELECT ExpenseID, UserID, Name, Type, Quantity, Price, Date 
                    FROM expensetable 
                    WHERE UserID = %s
                """, (current_user,))
                expenses = cursor.fetchall()
                self.main_db.commit()
                cursor.close()
            else:
                expenses = self.return_all_expenses()
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

    def remove_given_users(self, current_user, given_user_ids):
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

    def return_all_incomes(self):
        try:
            cursor = self.main_db.cursor(dictionary=True)
            query = """SELECT UserID, Level, Salary
            FROM salarytable"""
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as given_error:
            return given_error

    def update_expense_in_db(self, changes, edit_expenses=None, edit_users=None, edit_income=None):
        try:
            cursor = self.main_db.cursor()
            updates = []
            params = []

            if edit_expenses is not None:
                query = """UPDATE expensetable SET """
                if 'Name' in changes:
                    updates.append("Name = %s")
                    params.append(changes['Name'])
                if 'Quantity' in changes:
                    updates.append("Quantity = %s")
                    params.append(changes['Quantity'])
                if 'Price' in changes:
                    updates.append("Price = %s")
                    params.append(changes['Price'])
                if 'Type' in changes:
                    updates.append("Type = %s")
                    params.append(changes['Type'])

                if updates:
                    query += ", ".join(updates) + " WHERE ExpenseID = %s;"
                    params.append(changes['ID'])
                    cursor.execute(query, tuple(params))
                else:
                    raise ValueError("No fields to update for income.")

            elif edit_users is not None:
                query = """UPDATE usertable SET """
                if 'FirstName' in changes:
                    updates.append("FirstName = %s")
                    params.append(changes['FirstName'])
                if 'LastName' in changes:
                    updates.append("LastName = %s")
                    params.append(changes['LastName'])
                if 'Email' in changes:
                    updates.append("Email = %s")
                    params.append(changes['Email'])
                if 'PhoneNumber' in changes:
                    updates.append("PhoneNumber = %s")
                    params.append(changes['PhoneNumber'])

                if updates:
                    query += ", ".join(updates) + " WHERE UserID = %s;"
                    params.append(changes['ID'])
                    cursor.execute(query, tuple(params))

                query = """UPDATE salarytable SET """
                updates = []
                params = []
                if 'Level' in changes:
                    updates.append("Level = %s")
                    params.append(changes['Level'])
                if 'Salary' in changes:
                    updates.append("Salary = %s")
                    params.append(changes['Salary'])

                if updates:
                    query += ", ".join(updates) + " WHERE UserID = %s;"
                    params.append(changes['ID'])
                    cursor.execute(query, tuple(params))
                else:
                    raise ValueError("No fields to update for user.")

            elif edit_income is not None:
                query = """UPDATE salarytable SET """
                if 'Level' in changes:
                    updates.append("Level = %s")
                    params.append(changes['Level'])
                if 'Salary' in changes:
                    updates.append("Salary = %s")
                    params.append(changes['Salary'])

                if not updates:
                    raise ValueError("No fields to update for income.")

                query += ", ".join(updates) + " WHERE UserID = %s;"
                params.append(changes['ID'])
                cursor.execute(query, tuple(params))

            self.main_db.commit()
            cursor.close()
            return "Successfully updated the database."
        except Exception as e:
            return e

    def insert_data_into_database(self, data, selection, callback_function):
        cursor = self.main_db.cursor()

        if selection == "Expenses":
            # Preparing the values for inserting expenses
            values = [
                (
                    row['ExpenseID'], row['UserID'], row['Name'], row['Type'],
                    row['Quantity'], row['Price'], row['Date']
                )
                for _, row in data.iterrows()
            ]
            query = """
            INSERT INTO expensetable (ExpenseID, UserID, Name, Type, Quantity, Price, Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            try:
                cursor.executemany(query, values)
                self.main_db.commit()
                cursor.close()
                MyMessageBoxes.ShowMessage().show_info("Successfully imported expenses")
                callback_function()
            except Exception as error:
                raise RuntimeError(f"Database error: {error}")

        elif selection == "Users":
            # Preparing the values for inserting users (UserID, FirstName, LastName, Email, etc.)
            user_values = [
                (
                    row['UserID'], row['FirstName'], row['LastName'], row['Email'],
                    row['PhoneNumber'], row['HashedPassword']
                )
                for _, row in data.iterrows()
            ]

            # Prepare salary values (UserID, Level, Salary)
            salary_values = [
                (
                    row['UserID'], row['Level'], row['Salary']
                )
                for _, row in data.iterrows()
            ]

            # Insert user data into 'usertable'
            first_query = """
            INSERT INTO usertable (UserID, FirstName, LastName, Email, PhoneNumber, HashedPassword)
            VALUES (%s, %s, %s, %s, %s, %s);
            """

            # Insert salary data into 'salarytable'
            second_query = """
            INSERT INTO salarytable (UserID, Level, Salary) VALUES (%s, %s, %s);
            """

            try:
                # Insert user data first
                cursor.executemany(first_query, user_values)

                # Insert salary data second
                cursor.executemany(second_query, salary_values)

                # Commit the changes to the database
                self.main_db.commit()
                cursor.close()

                # Inform the user that the import was successful
                MyMessageBoxes.ShowMessage().show_info("Successfully imported users and salaries")
                callback_function()

            except Exception as error:
                raise RuntimeError(f"Database error: {error}")

    def return_user_hashed_password(self, given_user):
        try:
            cursor = self.main_db.cursor()
            query = """SELECT HashedPassword FROM usertable WHERE UserID = %s;"""
            cursor.execute(query, (given_user, ))
            hashed_pass = cursor.fetchone()[0]
            cursor.close()
            return hashed_pass
        except Exception as error:
            return error

    def wipe_database(self):
        try:
            cursor = self.main_db.cursor()
            # Define the queries to wipe each table
            queries = [
                "DELETE FROM expensetable;",
                "DELETE FROM salarytable;",
                "DELETE FROM usertable;"]
            # Execute each query in sequence
            for query in queries:
                cursor.execute(query)
            # Commit the changes to the database
            self.main_db.commit()
            cursor.close()
            MyMessageBoxes.ShowMessage().show_info("Database successfully wiped.")
            return True
        except Exception as error:
            MyMessageBoxes.ShowMessage.show_info(f"Error wiping database: {error}")


class ExpenseViewer:
    def __init__(self, user_id, parent, submit_frame, on_remove_callback, show_users=None):
        self.__parent = parent
        self.spreadsheet_frame = ctk.CTkFrame(parent)
        self.spreadsheet_frame.pack(expand=True, fill='both')
        self.db = AccountsDatabase()
        self.user_id = user_id
        self.show_users = show_users
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
            self.scrollable_frame = ctk.CTkScrollableFrame(self.spreadsheet_frame)
            self.scrollable_frame.pack(fill="both", expand=True)

            # Column headers
            if self.show_users:
                headers = ["Select", "UserID", "FirstName", "LastName", "Email", "PhoneNumber", "Level", "Salary"]
            elif not self.show_users and self.db.check_user_level(self.user_id) == 0:
                headers = ["Select", "ExpenseID", "Name", "Quantity", "Price", "Date"]
            else:
                headers = ["Select", "ExpenseID", "UserID", "Name", "Quantity", "Price", "Type", "Date"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 14, "bold"))
                label.grid(row=0, column=col, padx=10, pady=5)

            # Display expenses with checkboxes
            self.information_checkboxes = []
            self.display_information()

            # Submit button to handle selected expenses
            self.submit_button = ctk.CTkButton(submit_frame, text="Remove",
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
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Name"])).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Quantity"])).grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=f"${info['Price']:.2f}").grid(row=row, column=4, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Date"])).grid(row=row, column=5, padx=10)
            elif not self.show_users and self.db.check_user_level(self.user_id) == 1:
                self.information_checkboxes.append((checkbox_var, info["ExpenseID"]))

                # Labels for each data column
                ctk.CTkLabel(self.scrollable_frame, text=str(info["ExpenseID"])).grid(row=row, column=1, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["UserID"])).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Name"])).grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Quantity"])).grid(row=row, column=4, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=f"${info['Price']:.2f}").grid(row=row, column=5, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Type"])).grid(row=row, column=6, padx=10)
                ctk.CTkLabel(self.scrollable_frame, text=str(info["Date"])).grid(row=row, column=7, padx=10)
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
                self.show_users) else AccountsDatabase().remove_given_users(self.user_id, selected_information)
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
        self.show_users = show_users
        self.information = self.get_information()  # Fetch expenses based on the year filter

        # Frame for the Treeview display
        self.excel_spreadsheet_frame = ctk.CTkFrame(self.parent)
        self.excel_spreadsheet_frame.pack(fill="both", expand=True)

        if self.information:
            # Treeview setup for displaying expenses
            if not show_users:
                self.tree = ttk.Treeview(
                    self.excel_spreadsheet_frame,
                    columns=("ExpenseID", "UserID", "Name", "Quantity", "Price", "Type", "Date"),
                    show="headings",
                )
                # Define headings and center-align text below
                headings = [("ExpenseID", 30), ("UserID", 30), ("Name", 40), ("Quantity", 70), ("Price", 60),
                            ("Type", 50), ("Date", 100)]
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
                ctk.CTkLabel(self.excel_spreadsheet_frame, text="No data found for your user.\n Only admins can see"
                                                                " all expenses.").place(x=100, y=100)
            else:
                ctk.CTkLabel(self.excel_spreadsheet_frame, text="No data found in the database").place(relx=0.5, y=100)

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
                            expense.get("Name", ""),
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
            sheet.column_dimensions['F'].width = 10
            sheet.column_dimensions['G'].width = 15
            if not self.show_users:
                sheet.title = f"User Expenses {self.year if self.year else 'All'}"

                # Define the headers and write them to the first row
                headers = ["ExpenseID", "UserID", "Name", "Quantity", "Price", "Type", "Date"]
                sheet.append(headers)

                # Add expense data rows to the sheet
                for expense in self.information:
                    sheet.append([expense["ExpenseID"], expense["UserID"], expense["Name"], expense["Quantity"],
                                  expense["Price"], expense["Type"], expense["Date"]])

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


class ExpenseEditor:
    def __init__(self, user_id, parent, submit_frame, callback_function=lambda: None, show_expenses=None,
                 show_users=None, show_income=None):
        self.user = user_id
        self.parent = parent
        self.show_expenses = show_expenses
        self.show_users = show_users
        self.show_income = show_income
        self.callback_function = callback_function
        self.db = AccountsDatabase()

        # Main frame for editing
        self.edit_frame = ctk.CTkFrame(parent)
        self.edit_frame.pack(fill="both", expand=True)

        # Remove unnecessary excel_spreadsheet_frame
        # self.excel_spreadsheet_frame = ctk.CTkFrame(self.parent)
        # self.excel_spreadsheet_frame.pack(fill="both", expand=True)

        if self.show_users:
            self.to_edit = self.db.return_all_users()
        elif self.show_income:
            self.to_edit = self.db.return_all_incomes()
        elif not self.show_users and not self.show_income and self.db.check_user_level(user_id) == 1:
            self.to_edit = self.db.return_all_expenses()
        else:
            self.to_edit = self.db.return_expenses_from_user(user_id)

        if self.to_edit:
            # Scrollable frame for spreadsheet-like display
            self.scrollable_frame = ctk.CTkScrollableFrame(self.edit_frame)
            self.scrollable_frame.pack(fill="both", expand=True)

            # Display data and add submit button
            self.information_checkboxes = []
            self.entry_widgets = []
            self.display_edits()

            # Submit button
            self.submit_button = ctk.CTkButton(submit_frame, text="Edit",
                                               command=self.write_edits, width=200)
            self.submit_button.pack(padx=30, side='right')
        else:
            # No data available message
            ctk.CTkLabel(self.edit_frame, text="No expenses found from your user.\n Only admins can see all expenses.") \
                .place(x=100, y=100)

    def display_edits(self):
        # Clear the frame (if needed)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Determine the headers and data structure based on context
        if self.show_users:
            headers = ["UserID", "FirstName", "LastName", "Email", "PhoneNumber", "Level", "Salary"]
            editable_fields = ["FirstName", "LastName", "Email", "PhoneNumber", "Level", "Salary"]
        elif self.show_income:
            headers = ["UserID", "Level", "Salary"]
            editable_fields = ["Level", "Salary"]
        else:
            headers = ["ExpenseID", "UserID", "Name", "Quantity", "Price", "Type", "Date"]
            editable_fields = ["Name", "Quantity", "Price", "Type"]

        # Add headers
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5)

        # Add editable entries
        self.entry_widgets = []  # Track all entry widgets for validation
        for row, info in enumerate(self.to_edit, start=1):
            row_widgets = {}
            for col, header in enumerate(headers):
                key = header
                value = info.get(key, "")  # Fetch the value for the current header
                if header == "Type":
                    entry_options = ["Rent", "Utilities", "Salaries", "Insurance", "Equipment", "Supplies", "Marketing",
                                     "Services", "Training", "Travel", "Food", "Other"]
                    entry = ctk.CTkOptionMenu(self.scrollable_frame, values=entry_options, width=100)
                    entry.set(str(value))
                else:
                    entry = ctk.CTkEntry(self.scrollable_frame, width=80)
                    entry.insert(0, str(value))  # Pre-fill the entry box

                # Disable fields that should not be edited
                if key not in editable_fields:
                    entry.configure(state="disabled", text_color='grey')

                entry.grid(row=row, column=col, padx=10, pady=5)
                row_widgets[key] = entry

            self.entry_widgets.append(row_widgets)

    def write_edits(self):
        changes = []
        for original_data, row_widgets in zip(self.to_edit, self.entry_widgets):
            updated_data = {}
            for key, entry in row_widgets.items():
                new_value = entry.get()
                old_value = str(original_data.get(key, ""))

                # Record changes if there's a difference
                if new_value != old_value:
                    updated_data[key] = new_value

            if updated_data:
                updated_data["ID"] = original_data.get("ExpenseID") or original_data.get("UserID")
                changes.append(updated_data)
            # Placeholder for the database function
            for change in changes:
                if self.show_expenses:
                    self.db.update_expense_in_db(change, edit_expenses=True)
                elif self.show_income:
                    self.db.update_expense_in_db(change, edit_income=True)
                else:
                    self.db.update_expense_in_db(change, edit_users=True)
        if changes:
            MyMessageBoxes.ShowMessage().show_info("Successfully updated database")
            self.callback_function()
        else:
            MyMessageBoxes.ShowMessage().show_error("No edits detected")
