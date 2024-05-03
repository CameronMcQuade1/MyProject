import re
# Length checker
# Format checker
# Presence Checker
# Data type checker
# Password strength checker


class Validator:
    @staticmethod
    def length_checker(info, size, choice):
        # Choice 1: check if info == size
        # Choice 2: check if info >= size
        # Choice 3: check if info <= size
        if choice == 1:
            if len(info) == size:
                return True
            else:
                return False
        elif choice == 2:
            if len(info) >= size:
                return True
            else:
                return False
        elif choice == 3:
            if len(info) <= size:
                return True
            else:
                return False
        else:  # If the choice cannot be found, return False
            return False

    @staticmethod
    def format_checker(info, choice):
        # Choice 1: check if info is in email format
        if choice == 1:
            email_format = re.compile(r"^[A-Za-z\d]+(?:\.[A-Za-z\d]+)*@[A-Za-z\d]+(?:\.[A-Za-z\d]+)*$")
            if re.fullmatch(email_format, info):  # Check if the info entered matches the email format
                return True
            else:
                return False

    @staticmethod
    def presence_checker(info, choice):
        # Choice 1: check if data is there when it is supposed to be
        # Choice 2: check if data is there when it is not supposed to be
        if choice == 1:
            info = info.replace(" ", "")
            if info == "":
                return True
            else:
                return False
        if choice == 2:
            if info != "":
                return True
            else:
                return False

    @staticmethod
    def data_type_checker(info, supposed_type, choice):
        # Choice 1: Check if the data is the type it is supposed to be
        if choice == 1:
            if isinstance(info, supposed_type):
                return True
            else:
                return False

    @staticmethod
    def password_strength_checker(info, strength):
        #  Strength 1: Check if password is over 10 digits
        #  Strength 2: Check if the password is over 10 digits and contains a number
        #  Strength 3: Check if the password is over 10 digits, contains a number and a special character
        #  Strength 4: Check if the password is over 10 digits, contains a number, a special character and a capital
        special_characters = re.compile('[@_!#$%^&*()<>?/|}{~:]')
        if strength == 1:
            if len(info) >= 10:
                return True
            else:
                return False
        elif strength == 2:
            if len(info) >= 10 and bool(re.search(r'\d', info)) is True:
                return True
            else:
                return False
        elif strength == 3:
            if len(info) >= 10 and bool(re.search(r'\d', info)) is True and bool(
                    special_characters.search(info)) is True:
                return True
            else:
                return False
        elif strength == 4:
            if len(info) >= 10 and bool(re.search(r'\d', info)) is True and bool(
                    special_characters.search(info)) is True and bool(
                        re.match(r'\w*[A-Z]\w*', info)) is True:
                return True
            else:
                return False
        else:
            return False
