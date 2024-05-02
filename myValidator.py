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
        # Choice 2: pass#
        if choice == 1:
            import re
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
