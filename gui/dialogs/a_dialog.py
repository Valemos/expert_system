import tkinter as tk
from abc import abstractmethod


class ADialog(tk.Frame):

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.root = root
        self._submitted = False
        self.root.configure(padx=10, pady=10)

        self.frame_submit = tk.Frame(root)
        self.button_submit = tk.Button(self.frame_submit, text="Submit", command=self.handle_submit)
        self.button_cancel = tk.Button(self.frame_submit, text="Cancel", command=self.handle_cancel)

    @abstractmethod
    def pack_elements(self):
        pass

    @abstractmethod
    def get_dialog_fields(self):
        pass

    def get_not_submitted_result(self):
        return []

    def pack_dialog(self):
        self.pack_elements()
        self.button_submit.pack(side=tk.LEFT)
        self.button_cancel.pack(side=tk.RIGHT)
        self.frame_submit.pack(side=tk.BOTTOM)

    def handle_submit(self):
        self._submitted = True
        self.root.destroy()

    def handle_cancel(self):
        self._submitted = False
        self.root.destroy()

    def get_results(self):
        self.wait_window()
        if self._submitted:
            return self.get_dialog_fields()
        else:
            return self.get_not_submitted_result()
