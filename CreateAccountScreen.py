import customtkinter as ctk
import MyCustomFunctions
import PasswordHasher


class CreateAccount:
    def __init__(self):
        self.window = ctk.CTk()  # Creating a standalone window
        self.window.geometry('300x185+810+300')
        self.window.resizable(False, False)

        self.frames = []

        # CustomTkinter variables
        self.first_name = ctk.StringVar()
        self.last_name = ctk.StringVar()
        self.admin_var = ctk.BooleanVar()
        self.email = ctk.StringVar()
        self.phone_number = ctk.StringVar()
        self.password = ctk.StringVar()

        # Create frames
        self.create_frames()
        self.current_frame_index = 0
        self.show_frame(self.current_frame_index)

        self.window.mainloop()

    def create_frames(self):
        # Name Frame: First Name and Last Name Entry Boxes
        self.name_frame = ctk.CTkFrame(self.window)
        self.create_acc_label = ctk.CTkLabel(self.name_frame, width=150, text="Creating Account", font=('Calibri', 20))
        self.create_acc_label.place(anchor='center', relx=0.5, rely=0.15)
        self.first_name_entry = ctk.CTkEntry(self.name_frame, textvariable=self.first_name, width=150, height=30)
        self.first_name_entry.place(anchor="center", relx=0.5, rely=0.35)
        self.last_name_entry = ctk.CTkEntry(self.name_frame, textvariable=self.last_name, width=150, height=30)
        self.last_name_entry.place(anchor="center", relx=0.5, rely=0.525)
        self.phone_number_entry = ctk.CTkEntry(self.name_frame, textvariable=self.phone_number, width=150, height=30)
        self.phone_number_entry.place(anchor="center", relx=0.5, rely=0.7)

        # Details Frame: Email, Password Entry Boxes and Admin/User Checkbox
        self.details_frame = ctk.CTkFrame(self.window)
        self.email_entry = ctk.CTkEntry(self.details_frame, textvariable=self.email,
                                        width=150, height=30)
        self.email_entry.place(anchor="center", relx=0.5, rely=0.15)
        self.password_entry = ctk.CTkEntry(self.details_frame, textvariable=self.password, show='',
                                           width=150, height=30)
        self.password_entry.place(anchor="center", relx=0.5, rely=0.35)

        MyCustomFunctions.ShowHidePasswordWidget(self.details_frame, self.password_entry, 0.82, 0.35)

        self.admin_checkbox = ctk.CTkCheckBox(self.details_frame, text="Admin Account", variable=self.admin_var)
        self.admin_checkbox.place(anchor="center", relx=0.5, rely=0.55)

        # Custom EntryPlaceHolderText
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.first_name_entry, "First Name:")
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.last_name_entry, "Last Name:")
        MyCustomFunctions.EntryPlaceHolderText(self.name_frame, self.phone_number_entry, "Phone Number:")
        MyCustomFunctions.EntryPlaceHolderText(self.details_frame, self.email_entry, "Email:")
        MyCustomFunctions.EntryPlaceHolderText(self.details_frame, self.password_entry, "Password:")

        self.frames.append(self.name_frame)
        self.frames.append(self.details_frame)

        # Create the "Next" and "Back" buttons
        self.name_exit_button = ctk.CTkButton(self.name_frame, text="Exit", command=self.previous_frame, width=80)
        self.name_exit_button.place(anchor="center", relx=0.365, rely=0.9)

        self.name_next_button = ctk.CTkButton(self.name_frame, text="Next", command=self.next_frame, width=80)
        self.name_next_button.place(anchor="center", relx=0.635, rely=0.9)

        self.details_back_button = ctk.CTkButton(self.details_frame, text="Back", command=self.previous_frame, width=80)
        self.details_back_button.place(anchor="center", relx=0.365, rely=0.9)

        self.details_done_button = ctk.CTkButton(self.details_frame, text="Done", command=self.completed_form, width=80)
        self.details_done_button.place(anchor="center", relx=0.635, rely=0.9)

    def show_frame(self, index):
        for frame in self.frames:
            frame.pack_forget()
        self.frames[index].pack(expand=True, fill="both")

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

    def find_all_accounts(self):
        pass

    def completed_form(self):
        self.window.destroy()


if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # Optional: Set to 'light' or 'dark'
    ctk.set_default_color_theme("blue")  # Optional: Set color theme

    CreateAccount()  # Create an instance of the window
