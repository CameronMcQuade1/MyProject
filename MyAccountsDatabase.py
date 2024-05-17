import sqlite3


class AccountsDatabase:
    def __init__(self):
        try:
            self.connector = sqlite3.connect('AccountsDB.db')
            self.cursor = self.connector.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Accounts (
                    AccountID TEXT PRIMARY KEY, 
                    Password TEXT NOT NULL, 
                    StaffLevel INTEGER NOT NULL);""")
            self.connector.commit()
        except sqlite3.Error as e:
            self.return_error(e)
            return

    @staticmethod
    def return_error(e):
        return e

    def check_accounts_amount(self):
        try:
            return self.cursor.execute("""SELECT COUNT(*) FROM Accounts""").fetchone()[0]
        except sqlite3.Error as e:
            return e

    def create_root_account(self):
        self.cursor.execute("""INSERT INTO""")


if __name__ == "__main__":
    test_database = AccountsDatabase()
    print(test_database.check_accounts_amount())
