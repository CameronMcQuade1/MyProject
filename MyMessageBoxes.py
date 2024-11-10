from CTkMessagebox import CTkMessagebox


class ShowMessage:
    @staticmethod
    def show_info(message):
        msg = CTkMessagebox(title='Info:', message=message)
        msg.geometry("400x300+725+250")

    @staticmethod
    def show_warning(message):
        msg = CTkMessagebox(title="Warning!", message=message,
                            icon="warning", option_1="Cancel", option_2="Okay", option_3="Help")
        msg.geometry("300x185+800+400")
        return msg.get()

    @staticmethod
    def show_error(message):
        msg = CTkMessagebox(title="Error:", message=message, icon="cancel")

    @staticmethod
    def ask_question(message, option1, option2, option3):
        msg = CTkMessagebox(title="Question:", message=message,
                            icon="question", option_1=option1, option_2=option2, option_3=option3)
        msg.geometry("350x215+750+400")
        return msg.get()

