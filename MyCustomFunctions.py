class EntryPlaceHolderText:
    def __init__(self, parent, target, text):
        target.insert(0, text)
        parent.bind('<Button-1>', lambda event: parent.focus_set())
        target.bind('<Button-1>', lambda event: self.entry_focused(target, text))
        target.bind('<FocusOut>', lambda event: self.entry_unfocused(target, text))
        return

    @staticmethod
    def entry_focused(target, placeholder):
        if target.get() == placeholder:
            target.delete('0', 'end')
            target['fg'] = 'black'

    @staticmethod
    def entry_unfocused(target, placeholder):
        if target.get() == "":
            target.config(show='')
            target.insert(0, placeholder)
            target['fg'] = 'grey'


class ShowHidePassword:
    def __init__(self, target):
        if target.cget('fg') == 'black':
            target.config(show='' if target.cget('show') == '*' else '*')
        return
