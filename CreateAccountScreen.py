import tkinter as tk
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
        # Create first frame
        self.current_frame_index = 0
        self.create_frames()
        self.show_frame(self.current_frame_index)

    def create_frames(self):
        # Name Frame: First Name and Last Name Entry Boxes
        self.name_frame = tk.Frame(self.account_screen)
        self.first_name_entry = tk.Entry(self.name_frame, textvariable=self.first_name)
        self.first_name_entry.pack(pady=5)
        self.last_name_entry = tk.Entry(self.name_frame, textvariable=self.last_name)
        self.last_name_entry.pack(pady=5)

        # Details Frame: Email, Password Entry Boxes and Admin/User Checkbox
        self.details_frame = tk.Frame(self.account_screen)

        self.email_entry = tk.Entry(self.details_frame, textvariable=self.email)
        self.email_entry.pack(pady=5)
        self.password_entry = tk.Entry(self.details_frame, show='', textvariable=self.password)
        self.password_entry.pack(pady=5)

        self.admin_checkbox = tk.Checkbutton(self.details_frame, text="Admin Account", variable=self.admin_var)
        self.admin_checkbox.pack(pady=5)

        self.frames.append(self.name_frame)
        self.frames.append(self.details_frame)

        # Create the "Next" button
        self.next_button = tk.Button(self.account_screen, text="Next", command=self.next_frame)
        self.next_button.pack(side=tk.BOTTOM, pady=10)

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

    def find_all_accounts(self):
        pass

    def destroy_self(self):
        self.account_screen.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x185+500+150')
    account_frame = CreateAccount(root)
    root.mainloop()
