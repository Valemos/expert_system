import tkinter as tk

from gui.check_list import CheckList


class DialogSelectMachines(tk.Frame):

    def __init__(self, root, machines_names, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.root = root
        self._submitted = False

        self.machines_list = CheckList(root)
        self.machines_list.set_objects(machines_names)

        self.frame_submit = tk.Frame(root)
        self.button_submit = tk.Button(self.frame_submit, text="Submit", command=self.handle_submit)
        self.button_cancel = tk.Button(self.frame_submit, text="Cancel", command=self.handle_cancel)
        self.button_submit.pack(side=tk.LEFT)
        self.button_cancel.pack(side=tk.RIGHT)

        self.machines_list.pack(side=tk.TOP)
        self.frame_submit.pack(side=tk.TOP)

    def handle_submit(self):
        self._submitted = True
        self.root.destroy()

    def handle_cancel(self):
        self._submitted = False
        self.root.destroy()

    def get_selected(self):
        self.wait_window()
        if self._submitted:
            return self.machines_list.get_checked_objects()
        else:
            return []
