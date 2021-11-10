from tkinter_extension.menu.menu_object_selector_widget import MenuObjectSelectorWidget

import rules.production_config
from gui.dialogs.a_dialog import tk, ADialog
from object_types.part_rate import PartRate


class DialogProduce(ADialog):

    def __init__(self, root, part_rate: PartRate, **kw):
        super().__init__(root, **kw)
        self.part_rate = part_rate

        can_produce_brands = [b['brand'] for b in rules.get_machines_for_part(part_rate.name)]
        self.menu_select_brand = MenuObjectSelectorWidget(root, 20, can_produce_brands)
        self.pack_dialog()

    def pack_elements(self):
        tk.Label(self.root, text=f'Select machine for {self.part_rate.name}').pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_select_brand.pack(side=tk.TOP)

    def get_dialog_fields(self):
        return self.menu_select_brand.get()

    def get_not_submitted_result(self):
        return None
