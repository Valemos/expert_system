import tkinter as tk
from dataclasses import dataclass

import tkinter_extension.entry as entry
import tkinter_extension.widget_list as widget_list
from tkinter_extension.tk_context import TkContext


@dataclass
class PartRate:
    name: str
    rate: float


@dataclass
class MachineProperties:
    name: str
    cost: float
    produced_parts: list[PartRate]


class DialogNewMachine(tk.Frame):

    @classmethod
    def run_dialog(cls) -> MachineProperties:
        with TkContext() as dialog:
            return cls(dialog).get_properties()

    def __init__(self, root=None, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.root = root
        # self.root.wm_protocol("WM_DELETE_WINDOW", self.handle_cancel)
        self.root.title("New machine properties")
        self.root.configure(padx=5, pady=5)

        self._submitted = False

        self.entry_machine_name = entry.EntryWithLabel(self.root, "Machine name:", 20)
        self.entry_cost = entry.EntryFloatWithLabel(self.root, "Price:", 10)
        self.list_produced = widget_list.DynamicWidgetList(self.root, entry.EntryNameAmount, "Add production rate")

        self.frame_submit = tk.Frame(self.root)
        self.button_submit = tk.Button(self.frame_submit, text="Submit", command=self.handle_submit)
        self.button_cancel = tk.Button(self.frame_submit, text="Cancel", command=self.handle_cancel)
        self.button_submit.pack(side=tk.LEFT)
        self.button_cancel.pack(side=tk.RIGHT)

        self.entry_machine_name.pack(side=tk.TOP)
        self.entry_cost.pack(side=tk.TOP)
        self.list_produced.pack(side=tk.TOP)
        self.frame_submit.pack(side=tk.TOP)

    def handle_submit(self):
        self._submitted = True
        self.destroy()

    def handle_cancel(self):
        self._submitted = False
        self.destroy()

    def get_properties(self):
        self.wait_window()
        parts = [PartRate(name=i.get_name(), rate=i.get_amount()) for i in self.list_produced.iter_items]
        return MachineProperties(
            name=self.entry_machine_name.get(),
            cost=self.entry_cost.get(),
            produced_parts=parts)


if __name__ == '__main__':
    print(DialogNewMachine.run_dialog())
