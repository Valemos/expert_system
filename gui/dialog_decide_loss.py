from tkinter_extension.entry import EntryFloatWithLabel

from durable.lang import *
from gui.dialogs.a_dialog import tk, ADialog


class DialogDecideLoss(ADialog):

    def __init__(self, root, amount, **kw):
        super().__init__(root, **kw)
        self.loss = amount

        self.entry_additional_money = EntryFloatWithLabel(root, "Can add money", 20, 0)
        self.pack_dialog()

    def pack_elements(self):
        tk.Label(self.root, text="You have unmet losses").pack(side=tk.TOP)
        self.entry_additional_money.pack(side=tk.TOP)

    def get_dialog_fields(self):
        actions = []

        additional_money = self.entry_additional_money.get()
        if additional_money > 0:
            post('production', {'income': additional_money})
            actions.append(f'+{additional_money}u - Put your money')

        if self.loss > additional_money:
            actions.append(f'+{self.loss - additional_money}u - Take credit')

        return actions
