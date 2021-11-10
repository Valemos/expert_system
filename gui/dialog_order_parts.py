import tkinter

from tkinter_extension.widget_list import DynamicWidgetList

from gui.dialogs.a_dialog import ADialog
from gui.entry_menu_amount import EntryMenuAmount
from gui.name_amount_entry_list import NameAmountEntryList
from object_types.part_rate import PartRate


class PartRateWidgetList(DynamicWidgetList):

    def __init__(self, root, button_name, part_options):
        super().__init__(root, button_name)
        self._part_options = part_options

    def create_object_widget(self, wrapper, obj):
        if obj is None:
            item = EntryMenuAmount(wrapper, self._part_options)
            item.chosen = self._part_options[0]
            return item

        if not isinstance(obj, PartRate):
            raise ValueError("not a part rate")

        item = EntryMenuAmount(wrapper, self._part_options)
        item.chosen = obj.name
        item.amount = obj.name
        return item

    def create_empty(self):
        self.create_list_item(None)


class DialogOrderParts(ADialog):

    def __init__(self, root, possible_parts, **kw):
        super().__init__(root, **kw)

        self.parts_list = PartRateWidgetList(root, "Add new part", possible_parts)
        self.pack_dialog()

    def pack_elements(self):
        self.parts_list.pack(side=tkinter.TOP)

    def get_dialog_fields(self):
        return [PartRate(i.chosen, i.amount) for i in self.parts_list.iter_items]

    def get_results(self) -> list[PartRate]:
        return super().get_results()
