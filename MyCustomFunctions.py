from PIL import Image
import customtkinter as ctk


class EntryPlaceHolderText:
    def __init__(self, parent, target, text):
        # Insert the placeholder text and set text color to grey
        target.insert(0, text)
        target.configure(text_color='grey')

        # Bind events for placeholder functionality
        parent.bind('<Button-1>', lambda event: parent.focus_set())  # Focus parent
        target.bind('<FocusIn>', lambda event: self.entry_focused(target))
        target.bind('<FocusOut>', lambda event: self.entry_unfocused(target, text))

    @staticmethod
    def entry_focused(target):
        # If the text color is grey, it means it's showing the placeholder
        if target.cget('text_color') == 'grey':
            target.delete(0, 'end')  # Remove the placeholder
            target.configure(text_color='black')  # Set text color to black

    @staticmethod
    def entry_unfocused(target, placeholder):
        # If the entry box is empty, show the placeholder again
        if target.get() == "":
            target.insert(0, placeholder)
            target.configure(text_color='grey')  # Set text color to grey again
            target.configure(show='')


class ShowHidePasswordText:
    def __init__(self, target):
        if target.cget('text_color') == 'black':
            target.configure(show='' if target.cget('show') == '*' else '*')
        else:
            target.configure(show='')
        return


class ShowHidePasswordWidget:
    def __init__(self, parent, target, place_x, place_y):
        password_hidden_image_path = "PasswordHiddenImage.png"
        password_hidden_image = Image.open(password_hidden_image_path)
        password_hidden_image = password_hidden_image.resize((20, 20))  # Resize to fit button
        password_hidden_image = ctk.CTkImage(light_image=password_hidden_image, size=(20, 20))
        # Image which is shown when the password is shown
        password_shown_image_path = "PasswordShownImage.png"
        password_shown_image = Image.open(password_shown_image_path)
        password_shown_image = password_shown_image.resize((20, 20))  # Resize to fit button
        password_shown_image = ctk.CTkImage(light_image=password_shown_image, size=(20, 20))
        # Create the button with a proper size and rounded corners

        self.show_hide_password = ctk.CTkButton(parent, width=10, height=10, image=password_hidden_image,
                                                text="", corner_radius=20)

        self.show_hide_password.bind("<Button-1>", lambda event: self.show_hide_password.configure(
            image=password_shown_image) if self.show_hide_password.cget('image') == password_hidden_image else
            self.show_hide_password.configure(image=password_hidden_image))

        self.show_hide_password.bind('<ButtonPress-1>', lambda event: ShowHidePasswordText(
            target))

        self.show_hide_password.place(anchor='center', relx=place_x, rely=place_y)
        target.bind("<Button-1>", lambda event: target.configure(
            show='*') if self.show_hide_password.cget('image') == password_hidden_image else
            target.configure(show=''))

