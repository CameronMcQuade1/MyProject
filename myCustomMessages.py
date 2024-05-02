from CTkMessagebox import CTkMessagebox
from customtkinter import CTk


class CustomMessage:
    CTk()

    @staticmethod
    def show_info(message):
        show_info = CTkMessagebox(title="Information:", message=message)
        show_info.mainloop()

    @staticmethod
    def show_success(message):
        show_success = CTkMessagebox(title="Success:", message=message, icon="check")
        show_success.mainloop()

    @staticmethod
    def show_error(message):
        show_error = CTkMessagebox(title="Error:", message=message, icon="cancel", option_1="Retry", option_2="Cancel")
        show_error.mainloop()

    @staticmethod
    def show_warning(message):
        show_warning = CTkMessagebox(title="Warning:", message=message, icon="warning",
                                     option_1="Cancel", option_2="Retry")
        show_warning.mainloop()

    @staticmethod
    def ask_question(message):
        ask_question = CTkMessagebox(title="Question:", message=message, icon="question",
                                     option_1="Cancel", option_2="No", option_3="Yes")
        ask_question.mainloop()
