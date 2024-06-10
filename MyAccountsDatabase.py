import sqlite3
import PasswordHasher


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
            __num_of_accounts = self.cursor.execute("""SELECT COUNT(*) FROM Accounts""").fetchone()[0]
            return __num_of_accounts
        except sqlite3.Error as e:
            return e

    def create_root_account(self):
        if self.check_accounts_amount() == 0:
            try:
                __root_password = self.create_root_password()
                self.cursor.execute("""INSERT INTO Accounts (AccountID, Password, StaffLevel)
                 VALUES ('Root', ?, 1)""", (__root_password,))
                self.connector.commit()
                return __root_password
            except sqlite3.Error as e:
                return e

    @staticmethod
    def create_root_password():
        __password = PasswordHasher.Hasher().create_random_password()
        return __password
