import tkinter
from typing import Iterator

from tkinter_extension.entry import EntryNameAmount
from tkinter_extension.widget_list import DynamicWidgetList

from object_types.part_rate import PartRate


class NameAmountEntryList(DynamicWidgetList):

    iter_items: Iterator[EntryNameAmount]

    def __init__(self, root, button_name):
        super().__init__(root, button_name)

    def create_object_widget(self, wrapper, obj):
        entry = EntryNameAmount(wrapper)
        self.button_new_widget.lift()

        if isinstance(obj, PartRate):
            entry.set_name(obj.name)
            entry.set_amount(obj.amount)
        elif isinstance(obj, str):
            entry.set_name(obj)

        return entry

    def create_empty(self):
        self.create_list_item('')
