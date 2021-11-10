from tkinter_extension.entry import EntryFloatWithLabel

from gui.dialogs.a_dialog import tk, ADialog


class DialogDecideLoss(ADialog):

    def __init__(self, root, amount, **kw):
        super().__init__(root, **kw)
        self.loss = amount

        self.entry_can_add_money = EntryFloatWithLabel(root, "Can add money", 20, 0)

    def pack_elements(self):
        tk.Label(self.root, text="You have unmet losses").pack(side=tk.TOP)
        self.entry_can_add_money.pack(side=tk.TOP)

    def get_dialog_fields(self):
        actions = []

        can_add = self.entry_can_add_money.get()
        if can_add > 0:
            actions.append(f'+{can_add}u - Put your money')

        actions.append(f'+{self.loss - can_add}u - Take credit')
        return actions
