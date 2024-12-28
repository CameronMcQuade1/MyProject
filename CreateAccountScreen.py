import customtkinter as ctk
import LoginScreen
import MyExpenseWindow
import MyCustomFunctions
import MyDatabase
import MyMessageBoxes
import MyValidator
import PasswordHasher
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class CreateAccount:
    def __init__(self, parent, current_user=None):
        self.parent = parent
        self.current_user = current_user
        self.parent.geometry("325x175+750+250")
        self.create_account_screen = ctk.CTkFrame(self.parent)

        self.frames = []

        # CustomTkinter variables
        self.__first_name = ctk.StringVar()
        self.__last_name = ctk.StringVar()
        self.__admin_var = ctk.BooleanVar()
        self.__email = ctk.StringVar()
        self.__phone_number = ctk.StringVar()
        self.__password = ctk.StringVar()
        self.__salary = ctk.StringVar()
        self.__verification_code = ctk.StringVar()
        self.__password_verification = ctk.StringVar()
        self.__random_code = random.randint(100000, 999999)

        # Create frames
        self.create_frames()
        self.current_frame_index = 0
        self.show_frame(self.current_frame_index)

        self.create_account_screen.pack(expand=True, fill=ctk.BOTH)

    def create_frames(self):
        # Name Frame: First Name and Last Name Entry Boxes
        self.name_frame = ctk.CTkFrame(self.create_account_screen)
        self.create_acc_label = ctk.CTkLabel(self.name_frame, width=150, text="Creating Account", font=('Calibri', 20))
        self.create_acc_label.place(anchor='center', relx=0.5, rely=0.15)
        self.first_name_entry = ctk.CTkEntry(self.name_frame, textvariable=self.__first_name, width=150, height=30)
        self.first_name_entry.place(anchor="center", relx=0.5, rely=0.35)
        self.last_name_entry = ctk.CTkEntry(self.name_frame, textvariable=self.__last_name, width=150, height=30)
        self.last_name_entry.place(anchor="center", relx=0.5, rely=0.525)
        self.phone_number_entry = ctk.CTkEntry(self.name_frame, textvariable=self.__phone_number, width=150, height=30)
        self.phone_number_entry.place(anchor="center", relx=0.5, rely=0.7)

        # Details Frame: Email, Password Entry Boxes and Admin/User Checkbox
        self.details_frame = ctk.CTkFrame(self.create_account_screen)
        self.email_entry = ctk.CTkEntry(self.details_frame, textvariable=self.__email,
                                        width=150, height=30)
        self.email_entry.place(anchor="center", relx=0.5, rely=0.15)
        self.password_entry = ctk.CTkEntry(self.details_frame, textvariable=self.__password, show='',
                                           width=150, height=30)
        self.password_entry.place(anchor="center", relx=0.5, rely=0.35)

        MyCustomFunctions.ShowHidePasswordWidget(self.details_frame, self.password_entry, 0.82, 0.35)

        self.salary_entry = ctk.CTkEntry(self.details_frame, textvariable=self.__salary, width=150, height=30)
        self.salary_entry.place(anchor="center", relx=0.5, rely=0.55)

        self.admin_checkbox = ctk.CTkCheckBox(self.details_frame, text="Admin Account", variable=self.__admin_var)
        self.admin_checkbox.place(anchor="center", relx=0.5, rely=0.725)

        if not MyDatabase.AccountsDatabase().return_account_amount():
            self.admin_checkbox.select()
            self.admin_checkbox.configure(state='disabled')

        # Custom EntryPlaceHolderText
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.first_name_entry, "First Name:")
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.last_name_entry, "Last Name:")
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.phone_number_entry, "Phone Number:")
        MyCustomFunctions.EntryPlaceHolderText(self.details_frame, self.email_entry, "Email:")
        MyCustomFunctions.EntryPlaceHolderText(self.details_frame, self.password_entry, "Password:")
        MyCustomFunctions.EntryPlaceHolderText(self.details_frame, self.salary_entry, "Salary:")

        self.frames.append(self.name_frame)
        self.frames.append(self.details_frame)

        # Create the "Next" and "Back" buttons
        self.name_exit_button = ctk.CTkButton(self.name_frame, text="Exit", command=self.exit_button_return, width=80)
        self.name_exit_button.place(anchor="center", relx=0.365, rely=0.9)

        self.name_next_button = ctk.CTkButton(self.name_frame, text="Next", command=self.next_frame, width=80)
        self.name_next_button.place(anchor="center", relx=0.635, rely=0.9)

        self.details_back_button = ctk.CTkButton(self.details_frame, text="Back", command=self.previous_frame, width=80)
        self.details_back_button.place(anchor="center", relx=0.365, rely=0.9)

        self.details_done_button = ctk.CTkButton(self.details_frame, text="Submit", command=self.completed_form,
                                                 width=80)
        self.details_done_button.place(anchor="center", relx=0.635, rely=0.9)

    def show_frame(self, index):
        for frame in self.frames:
            frame.pack_forget()
        self.frames[index].pack(expand=True, fill="both")

    def exit_button_return(self):
        self.create_account_screen.destroy()
        self.parent.geometry('850x525+425+175')
        if self.current_user:
            if MyDatabase.AccountsDatabase().check_user_level(self.current_user) == 1:
                MyExpenseWindow.AdminWindow(self.parent, self.current_user, "Accounts")
            else:
                MyExpenseWindow.DefaultWindow(self.parent, self.current_user)



    def next_frame(self):
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            self.show_frame(self.current_frame_index)

    def previous_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.show_frame(self.current_frame_index)

    def show_hide_password(self):
        MyCustomFunctions.ShowHidePasswordText(self.password_entry)

    def completed_form(self):
        first_name = self.__first_name.get()
        last_name = self.__last_name.get()
        email = self.__email.get()
        phone_number = self.__phone_number.get()
        password = self.__password.get()
        admin = self.__admin_var.get()
        salary = self.__salary.get()
        user_count = MyDatabase.AccountsDatabase().return_account_amount() + 1
        user_id = f"{first_name[0].upper()}{last_name[0].upper()}{user_count:04d}"

        def validate_details():
            correct_validation = (True, True, True, True, True, True, True, True)
            if ((MyValidator.Validator().presence_checker(first_name, 2),
                 MyValidator.Validator().presence_checker(last_name, 2),
                 MyValidator.Validator().length_checker(first_name, 30, 3),
                 MyValidator.Validator().length_checker(last_name, 30, 3),
                 MyValidator.Validator().format_checker(email, 1),
                 MyValidator.Validator().length_checker(phone_number, 11, 1),
                 MyValidator.Validator.password_strength_checker(password, 1),
                 MyValidator.Validator().presence_checker(salary, 2))
                    == correct_validation):

                hashed_password = PasswordHasher.Hasher().hash_password(password)
                self.create_account_screen.destroy()
                test_verification = self.two_factor_auth()
                if test_verification:
                    MyDatabase.AccountsDatabase().add_user_to_db(user_id, first_name, last_name, email,
                                                                 phone_number, hashed_password, admin, salary)
                    self.parent.geometry("850x525+425+175")
                    MyMessageBoxes.ShowMessage().show_info("Account Created - Your account ID has been emailed to you!")
                    self.email_user("Account ID",
                                    f"Your Account ID: {user_id}")
                    LoginScreen.MainLogin(self.parent)
                else:
                    CreateAccount(self.parent)
            else:
                MyMessageBoxes.ShowMessage().show_info(f"- First & Last name <= 30 characters \n"
                                                       "- Email must be in correct format \n"
                                                       "- Phone number must be 11 characters starting with 0 \n"
                                                       "- User's passwords must be over 10 characters and contain"
                                                       " a capital letter, number and special character. \n"
                                                       "- Salary cannot be left empty.")

        validate_details()

    def two_factor_auth(self):
        verification_result = ctk.BooleanVar()
        MyMessageBoxes.ShowMessage().show_info("- A verification code has been sent to the email you provided. \n"
                                               "- Please verify your details so your account can be created.")
        self.create_account_screen.destroy()
        verification_frame = ctk.CTkFrame(self.parent)
        verification_frame.pack(expand=True, fill="both")
        enter_code = ctk.CTkLabel(verification_frame, text="Enter Verification Code:", font=('Calibri', 20))
        enter_code.place(anchor="center", relx=0.5, rely=0.15)
        code_entry = ctk.CTkEntry(verification_frame, width=150)
        code_entry.place(anchor="center", relx=0.5, rely=0.3)
        enter_password = ctk.CTkLabel(verification_frame, text="Re-enter Password:", font=('Calibri', 20))
        enter_password.place(anchor="center", relx=0.5, rely=0.5)
        password_entry = ctk.CTkEntry(verification_frame, width=150)
        password_entry.place(anchor="center", relx=0.5, rely=0.65)
        MyCustomFunctions.ShowHidePasswordWidget(verification_frame, password_entry, 0.8, 0.65)
        MyCustomFunctions.EntryPlaceHolderText(verification_frame, code_entry, "Code:")
        MyCustomFunctions.EntryPlaceHolderText(verification_frame, password_entry, "Password:")
        back_button = ctk.CTkButton(verification_frame, text="Back", width=100, command=lambda: go_back())
        back_button.place(anchor="center", relx=0.3, rely=0.9)
        verify_button = ctk.CTkButton(verification_frame, text="Verify", width=100, command=lambda: try_verify())
        verify_button.place(anchor="center", relx=0.7, rely=0.9)

        # Send the email
        self.email_user("Verification Code", f"Enter the following code into the box: "
                                             f"{self.__random_code}")

        def go_back():
            verification_result.set(False)
            verification_frame.destroy()

        def try_verify():
            if (code_entry.get() == str(self.__random_code)) and (password_entry.get() == self.__password.get()):
                verification_result.set(True)
                verification_frame.destroy()
            else:
                MyMessageBoxes.ShowMessage().show_error("Incorrect details.\nRetry or go back.")

        self.parent.wait_variable(verification_result)  # Block until `verification_result` is set
        return verification_result.get()

    def email_user(self, email_subject, email_body):
        try:
            with smtplib.SMTP("smtp.mailersend.net", 587) as server:
                sender_email = "MS_AElKUp@trial-k68zxl2x8k9gj905.mlsender.net"
                sender_pass = "T1vHXqPbVSwTndFU"
                receiver_email = str(self.__email.get())

                subject = email_subject
                verification_code = random.randint(100000, 999999)
                body = email_body

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))
                # Replace with your SMTP server and port
                server.starttls()  # Secure the connection
                server.login(sender_email, sender_pass)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            MyMessageBoxes.ShowMessage().show_error(f"Error: {e}")



if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # Optional: Set to 'light' or 'dark'
    ctk.set_default_color_theme("blue")  # Optional: Set color theme
    root = ctk.CTk()
    root.geometry("325x175+750+250")
    CreateAccount(root, "CM0000")
    root.mainloop()
