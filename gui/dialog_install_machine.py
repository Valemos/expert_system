import tkinter as tk

from tkinter_extension.menu import MenuObjectSelectorWidget
from tkinter_extension.menu.menu_with_handler_widget import MenuWithHandlerWidget
from tkinter_extension.entry.float_with_label import EntryFloatWithLabel

from gui.dialogs.a_dialog import ADialog
from gui.entry_menu_amount import EntryMenuAmount
from object_types.assigned_machine import AssignedMachine
from object_types.machine_properties import MachineProperties
from object_types.part_rate import PartRate


class DialogInstallMachine(ADialog):

    def __init__(self, root, brands: list[MachineProperties], **kw):
        super().__init__(root, **kw)
        self._brands = {machine.brand: machine for machine in brands}
        brand_names = list(self._brands.keys())
        self.menu_brand = MenuWithHandlerWidget(root, 15, brand_names, self.handle_brand_selected)
        self.entry_part_rate = EntryMenuAmount(root)
        self.pack_dialog()

        self.menu_brand.choose_name(brand_names[0])

    def handle_brand_selected(self, choice):
        brand = self._brands[choice]
        self.entry_part_rate.set_choices(list(p.name for p in brand.produced_parts))
        self.entry_part_rate.menu_selection.choose_name(brand.produced_parts[0].name)

    def pack_elements(self):
        self.menu_brand.pack(side=tk.TOP)
        tk.Label(self, text="Produced part").pack(side=tk.TOP, anchor=tk.CENTER)
        self.entry_part_rate.pack(side=tk.TOP)

    def get_dialog_fields(self):
        return AssignedMachine(
            identifier=0,
            brand=self.menu_brand.get_string(),
            part_rate=PartRate(
                self.entry_part_rate.chosen,
                self.entry_part_rate.amount,
            )
        )

    def get_results(self) -> AssignedMachine:
        return super().get_results()


