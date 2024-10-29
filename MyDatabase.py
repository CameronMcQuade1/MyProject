import mysql.connector
import PasswordHasher
import customtkinter as ctk


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
                HashedPassword CHAR(30) NOT NULL
            )
        """)

        # Table 2: SalaryTable with One-to-One relationship with UserTable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS SalaryTable (
                UserID VARCHAR(6),
                Level INT NOT NULL,
                Salary DECIMAL(10, 2) NOT NULL,
                PRIMARY KEY (UserID, Level),
                FOREIGN KEY (UserID) REFERENCES UserTable(UserID) ON DELETE CASCADE
            )
        """)

        # Table 3: ExpenseTable with One-to-Many relationship with UserTable
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS ExpenseTable (
                ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
                UserID VARCHAR(6),
                Quantity INT NOT NULL,
                Price DECIMAL(10, 2) NOT NULL,
                Date DATE NOT NULL,
                FOREIGN KEY (UserID) REFERENCES UserTable(UserID) ON DELETE CASCADE
            )
        """)

        db_cursor.close()
        self.main_db.database = "ExpenseDatabase"

    @staticmethod
    def bad_connection(given_error):
        return given_error

    @staticmethod
    def return_balance(self):
        pass

    def return_expenses_from_user(self, current_user):
        cursor = self.main_db.cursor(dictionary=True)
        cursor.execute("""
                    SELECT ExpenseID, Quantity, Price, Date 
                    FROM ExpenseTable 
                    WHERE UserID = %s
                """, (current_user,))
        expenses = cursor.fetchall()
        cursor.close()
        return expenses


class ExpenseViewer(ctk.CTk):
    def __init__(self, db, user_id, parent):
        super().__init__(parent)  # Set the parent for the CTk instance
        self.db = AccountsDatabase
        self.user_id = user_id
        self.title("Expense Tracker")
        self.geometry("600x400")

        # Create a frame to hold the scrollable frame
        self.frame = ctk.CTkFrame(self)  # Create a frame as the main container
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Scrollable frame for spreadsheet-like display
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame, width=580, height=300)
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
        self.submit_button = ctk.CTkButton(self.frame, text="Submit", command=self.get_selected_expenses)
        self.submit_button.pack(pady=10)

    def display_expenses(self):
        expenses = self.db.get_user_expenses(self.user_id)

        for row, expense in enumerate(expenses, start=1):
            # Checkbox for each expense
            checkbox_var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.scrollable_frame, variable=checkbox_var)
            checkbox.grid(row=row, column=0, padx=10, pady=5)
            self.expense_checkboxes.append((checkbox_var, expense["ExpenseID"]))

            # Labels for each data column
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["ExpenseID"])).grid(row=row, column=1, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["Quantity"])).grid(row=row, column=2, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=f"${expense['Price']:.2f}").grid(row=row, column=3, padx=10)
            ctk.CTkLabel(self.scrollable_frame, text=str(expense["Date"])).grid(row=row, column=4, padx=10)

    def get_selected_expenses(self):
        selected_expenses = [expense_id for var, expense_id in self.expense_checkboxes if var.get()]
        print("Selected Expenses:", selected_expenses)  # Handle the selected expenses as needed


if __name__ == '__main__':
    test_db = AccountsDatabase()
    test_db.create_tables()
