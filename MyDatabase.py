import mysql.connector
import PasswordHasher


class AccountsDatabase:
    def __init__(self):
        try:
            self.main_db = mysql.connector.connect(
                host='127.0.0.1',
                user='admin',
                password='rcV])R%tN3YnS"b')
        except mysql.connector.errors.ProgrammingError as e:
            self.bad_connection(e)

    def create_tables(self):
        db_cursor = self.main_db.cursor()
        db_cursor.execute("CREATE SCHEMA IF NOT EXISTS ExpenseDatabase")
        db_cursor.execute("USE ExpenseDatabase")
        db_cursor.execute("CREATE TABLE IF NOT EXISTS UserTable"
                          "(UserID VARCHAR(6) PRIMARY KEY,"
                          "FirstName CHAR(30) NOT NULL,"
                          "LastName CHAR(30) NOT NULL,"
                          "Email VARCHAR(256) NOT NULL,"
                          "PhoneNumber CHAR(11) NOT NULL,"
                          "HashedPassword VARCHAR(256) NOT NULL)")
        db_cursor.execute("CREATE TABLE IF NOT EXISTS ExpenseTable"
                          "(ExpenseID AUTONUM )")
        db_cursor.close()
        self.main_db.database = "ExpenseDatabase"

    @staticmethod
    def bad_connection(given_error):
        return given_error

    @staticmethod
    def return_balance(self):
        pass

if __name__ == '__main__':
    test_db = AccountsDatabase()
    test_db.create_tables()
