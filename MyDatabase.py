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
        self.main_db.database = "ExpenseDatabase"

    @staticmethod
    def bad_connection(given_error):
        return given_error
