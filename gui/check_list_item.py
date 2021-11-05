import tkinter as tk


class CheckListItem(tk.Frame):

    def __init__(self, root, label, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.label = label
        self._state = tk.IntVar()
        self._checkbutton = tk.Checkbutton(self, text=label, variable=self._state)
        self._checkbutton.pack(side=tk.LEFT)

    @property
    def checked(self):
        return self._state == 1
