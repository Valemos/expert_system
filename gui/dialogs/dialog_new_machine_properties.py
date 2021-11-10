import tkinter as tk

from tkinter_extension.entry import EntryWithLabel, EntryFloatWithLabel
from tkinter_extension.tk_context import TkContext

from gui.dialogs.a_dialog import ADialog
from gui.name_amount_entry_list import NameAmountEntryList
from object_types.machine_properties import MachineProperties
from object_types.part_rate import PartRate


class DialogNewMachine(ADialog):
    def __init__(self, root=None, **kw):
        super().__init__(root, **kw)
        self.root.title("New machine properties")

        self.entry_machine_brand = EntryWithLabel(root, "Machine brand:", 20)
        self.entry_cost = EntryFloatWithLabel(root, "Price:", 20, 0)

        self.list_produced = NameAmountEntryList(root, "Add production rate")

    def pack_elements(self):
        self.entry_machine_brand.pack(side=tk.TOP, anchor=tk.E)
        self.entry_cost.pack(side=tk.TOP, anchor=tk.E)
        self.list_produced.pack(side=tk.TOP, anchor=tk.CENTER)

    def get_dialog_fields(self):
        parts = [PartRate(name=i.get_name(), amount=i.get_amount()) for i in self.list_produced.iter_items]
        return MachineProperties(
            brand=self.entry_machine_brand.get(),
            cost=self.entry_cost.get(),
            produced_parts=parts,
            needs_staff=True,
        )


if __name__ == '__main__':
    with TkContext() as dialog:
        results = DialogNewMachine(dialog).get_results()
    print(results)
