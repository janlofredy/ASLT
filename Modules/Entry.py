import tkinter as tk

class EntryWP(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', font=('bold',12)):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self['font'] = 'bold',12    

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self['font'] = 'bold',12

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()