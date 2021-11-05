import tkinter as tk

from tkinter_extension.widget_list import FixedWidgetList
from tkinter_extension.widget_list.list_item_widget import ListItemWidget

from gui.check_list_item import CheckListItem


class CheckList(FixedWidgetList):

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.options = {}

    def pack_object_to_item(self, wrapper: ListItemWidget, obj):
        label = str(obj)
        self.options[label] = obj

        item = CheckListItem(wrapper, label, width=30)
        item.pack(side=tk.LEFT)
        return item

    def get_checked_objects(self):
        return [self.options[w.label] for w in self.iter_items if w.checked]
