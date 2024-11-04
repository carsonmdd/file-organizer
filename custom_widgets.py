import tkinter as tk

class CustomEntry(tk.Entry):
    def __init__(self, master, placeholder='', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.set_placeholder(None)
        self.bind('<FocusIn>', self.remove_placeholder)
        self.bind('<FocusOut>', self.set_placeholder)
        self.bind('<Left>', self.scroll_left)
        self.bind('<Right>', self.scroll_right)

    def set_placeholder(self, event):
        if self.placeholder and not self.get():
            self.insert(0, self.placeholder)
            self.config(fg='gray')
    
    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg='black')

    def scroll_left(self, event):
        self.xview_scroll(-1, 'units')
    
    def scroll_right(self, event):
        self.xview_scroll(1, 'units')