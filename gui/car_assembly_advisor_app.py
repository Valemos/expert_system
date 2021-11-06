import tkinter as tk

from gui.dialogs.dialog_select_machines import DialogSelectMachines


class CarAssemblyAdvisorApp(tk.Frame):

    def __init__(self, root=None, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.root = root
        self.winfo_toplevel().title("Assembly Advisor")
        self.root.configure(padx=10, pady=10)

        tk.Button(root, text="Machine Broke", command=self.handle_machine_broke).pack(side=tk.TOP, anchor=tk.NW)

    def handle_machine_broke(self):
        dialog = DialogSelectMachines(tk.Toplevel(self), ["hello", "world"])
        print(dialog.get_selected())
