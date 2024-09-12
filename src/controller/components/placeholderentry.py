import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._remove_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def _remove_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

