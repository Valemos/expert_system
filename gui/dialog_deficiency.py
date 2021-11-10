from enum import Enum

from durable.lang import *

from tkinter_extension.menu import MenuObjectSelectorWidget

import rules.shared
from gui.dialog_produce import DialogProduce
from gui.dialogs.a_dialog import tk, ADialog
from object_types.assigned_machine import AssignedMachine
from object_types.part_rate import PartRate


class DeficiencyDecision(Enum):
    MARKET = "market"
    PRODUCE = "produce"


class DialogDeficiency(ADialog):

    def __init__(self, root, part_rate: PartRate, **kw):
        super().__init__(root, **kw)
        self.part_rate = part_rate

        self.menu_options = MenuObjectSelectorWidget(root, 15, {e.value: e for e in DeficiencyDecision})
        self.pack_dialog()

    def pack_elements(self):
        tk.Label(self.root, text=f"Deal with deficiency\n{self.part_rate}").pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_options.pack(side=tk.TOP, anchor=tk.CENTER)

    def get_dialog_fields(self):
        option = self.menu_options.get()

        if DeficiencyDecision.MARKET == option:
            post('production', {'type': 'buy', 'part_rate': self.part_rate.to_json()})
            return f'Buy {self.part_rate} on market'
        elif DeficiencyDecision.PRODUCE == option:
            selected_machine = DialogProduce(tk.Toplevel(self.root.master), self.part_rate).get_results()
            if selected_machine is not None:
                assert_fact('machine', AssignedMachine(rules.get_next_machine_id(),
                                                       selected_machine,
                                                       self.part_rate, ).to_json())
                return f'Produce {self.part_rate}'
            else:
                return f'Ignore {self.part_rate}'

    def get_not_submitted_result(self):
        return None
