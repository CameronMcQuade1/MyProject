from tkinter import messagebox


class ShowMessage:

    @staticmethod
    def show_info(message):
        messagebox.showinfo(message)

    @staticmethod
    def show_warning(message):
        messagebox.showwarning(message)

    @staticmethod
    def show_error(message):
        messagebox.showerror(message)

    @staticmethod
    def ask_question(message):
        messagebox.askquestion(message)

    @staticmethod
    def ask_ok_cancel(message):
        messagebox.askokcancel(message)

    @staticmethod
    def ask_yes_no(message):
        messagebox.askyesno(message)

    @staticmethod
    def ask_retry(message):
        messagebox.askretrycancel(message)

