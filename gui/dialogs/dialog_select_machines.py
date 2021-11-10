import tkinter as tk

from gui.check_list import CheckList
from gui.dialogs.a_dialog import ADialog
from object_types.assigned_machine import AssignedMachine


class DialogSelectMachines(ADialog):

    def __init__(self, root, machines: list[AssignedMachine], **kw):
        super().__init__(root, **kw)

        self.machines_list = CheckList(root)
        self.machines_list.set_objects(machines)
        self.pack_dialog()

    def pack_elements(self):
        self.machines_list.pack(side=tk.TOP)
        self.frame_submit.pack(side=tk.TOP)

    def get_dialog_fields(self):
        return self.machines_list.get_checked_objects()

    def get_results(self) -> list[AssignedMachine]:
        return super().get_results()

