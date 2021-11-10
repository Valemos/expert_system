import rules
from gui.dialogs.a_dialog import tk, ADialog
from gui.entry_menu_amount import EntryMenuAmount
from object_types.part_rate import PartRate


class DialogBuyPart(ADialog):

    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        self.root.title("EnterPartRate")
        self.entry_name_amount = EntryMenuAmount(root, list(rules.production_config.market_prices.keys()))
        self.pack_dialog()

    def pack_elements(self):
        self.entry_name_amount.pack(side=tk.TOP)

    def get_dialog_fields(self):
        return PartRate(self.entry_name_amount.chosen, self.entry_name_amount.amount)

    def get_not_submitted_result(self):
        return None
