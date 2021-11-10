import tkinter as tk

from tkinter_extension.entry import EntryFloatWithLabel
from tkinter_extension.menu import MenuObjectSelectorWidget


class EntryMenuAmount(tk.Frame):

    def __init__(self, root, menu_objects=None, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.menu_selection = MenuObjectSelectorWidget(self, 10, menu_objects)
        self.entry_amount = EntryFloatWithLabel(self, "Amount", 10, 0)
        self.menu_selection.pack(side=tk.LEFT)
        self.entry_amount.pack(side=tk.LEFT)

    def set_choices(self, *args, **kwargs):
        self.menu_selection.set_objects(*args, **kwargs)

    @property
    def chosen(self):
        return self.menu_selection.get()

    @chosen.setter
    def chosen(self, option):
        self.menu_selection.set(option)

    @property
    def amount(self):
        return self.entry_amount.get()

    @amount.setter
    def amount(self, value):
        self.entry_amount.set(value)
