import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master, placeholder='', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.set_placeholder(None)
        self.bind('<FocusIn>', self.remove_placeholder)
        self.bind('<FocusOut>', self.set_placeholder)

    def set_placeholder(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg='gray')
    
    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg='black')