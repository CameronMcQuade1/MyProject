import tkinter as tk
from MyCustomFunctions import EntryPlaceHolderText, ShowHidePassword
import PasswordHasher


class CreateAccount:
    def __init__(self, parent):
        self.parent = parent
        self.account_screen = tk.Frame(parent)
        self.account_screen.pack(expand=True, fill=tk.BOTH)
        self.frames = []
        # Tk variables
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.admin_var = tk.BooleanVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        # Create frames
        self.create_frames()
        self.current_frame_index = 0
        self.show_frame(self.current_frame_index)

    def create_frames(self):
        # Name Frame: First Name and Last Name Entry Boxes
        self.name_frame = tk.Frame(self.account_screen)
        self.first_name_entry = tk.Entry(self.name_frame, textvariable=self.first_name, fg='grey')
        self.first_name_entry.place(anchor=tk.CENTER, relx=0.5, rely=0.15)
        self.last_name_entry = tk.Entry(self.name_frame, textvariable=self.last_name, fg='grey')
        self.last_name_entry.place(anchor=tk.CENTER, relx=0.5, rely=0.35)
        EntryPlaceHolderText(self.name_frame, self.first_name_entry, 'First Name')
        EntryPlaceHolderText(self.name_frame, self.last_name_entry, 'Last Name')

        # Details Frame: Email, Password Entry Boxes and Admin/User Checkbox
        self.details_frame = tk.Frame(self.account_screen)
        self.email_entry = tk.Entry(self.details_frame, textvariable=self.email, fg='grey')
        self.email_entry.place(anchor=tk.CENTER, relx=0.5, rely=0.15)
        EntryPlaceHolderText(self.details_frame, self.email_entry, 'Email')
        self.password_entry = tk.Entry(self.details_frame, show='', textvariable=self.password, fg='grey')
        self.password_entry.place(anchor=tk.CENTER, relx=0.5, rely=0.35)
        EntryPlaceHolderText(self.details_frame, self.password_entry, 'Password')
        self.admin_checkbox = tk.Checkbutton(self.details_frame, text="Admin Account", variable=self.admin_var)
        self.admin_checkbox.place(anchor=tk.CENTER, relx=0.5, rely=0.55)

        self.frames.append(self.name_frame)
        self.frames.append(self.details_frame)

        # Create the "Next" and "Back" buttons
        self.next_button = tk.Button(self.account_screen, text="Next", command=self.next_frame, width=5)
        self.next_button.place(anchor=tk.CENTER, relx=0.635, rely=0.85)

        self.back_button = tk.Button(self.account_screen, text="Back", command=self.previous_frame, width=5)
        self.back_button.place(anchor=tk.CENTER, relx=0.365, rely=0.85)

    def show_frame(self, index):
        for frame in self.frames:
            frame.pack_forget()
        self.frames[index].pack(expand=True, fill=tk.BOTH)
        if index == len(self.frames) - 1:
            self.next_button.config(text="Done", command=self.destroy_self)
        else:
            self.next_button.config(text="Next", command=self.next_frame)

    def next_frame(self):
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            self.show_frame(self.current_frame_index)

    def previous_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.show_frame(self.current_frame_index)

    def find_all_accounts(self):
        pass

    def destroy_self(self):
        self.account_screen.destroy()
        self.next_button.destroy()
        self.back_button.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x185+500+150')
    root.resizable(False, False)
    account_frame = CreateAccount(root)
    root.mainloop()
