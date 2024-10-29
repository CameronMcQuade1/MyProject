import mysql.connector
import PasswordHasher

import mysql.connector


class AccountsDatabase:
    def __init__(self):
        try:
            self.main_db = mysql.connector.connect(
                host='127.0.0.1',
                user='admin',
                password='rcV])R%tN3YnS"b'
            )
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
        pass


if __name__ == '__main__':
    test_db = AccountsDatabase()
    test_db.create_tables()
