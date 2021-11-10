import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from durable.lang import *
from json_annotated.raw_json import RawJson

import rules
from gui.ApplicationState import ApplicationState
from gui.dialog_install_machine import DialogInstallMachine

from gui.dialog_order_parts import DialogOrderParts
from gui.dialogs.dialog_select_machines import DialogSelectMachines
from object_types.assigned_machine import AssignedMachine


class CarAssemblyAdvisorApp(tk.Frame):

    state_file_path = Path('business_state.json')

    def __init__(self, root=None, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.root = root
        self.winfo_toplevel().title("Assembly Advisor")
        self.root.configure(padx=10, pady=10)

        tk.Button(root, text="Show status", command=self.handle_show_status).pack(side=tk.TOP, anchor=tk.CENTER)
        tk.Button(root, text="Install machine", command=self.handle_install_machine).pack(side=tk.TOP, anchor=tk.CENTER)
        tk.Button(root, text="Machine Broke", command=self.handle_machine_broke).pack(side=tk.TOP, anchor=tk.CENTER)
        tk.Button(root, text="Order parts", command=self.handle_order_parts).pack(side=tk.TOP, anchor=tk.CENTER)
        tk.Button(root, text="Save state", command=self.save_state).pack(side=tk.TOP, anchor=tk.CENTER)

        self.init_state()

    def init_state(self):
        if self.state_file_path.exists():
            with self.state_file_path.open('r') as fin:
                state = ApplicationState.from_json(json.load(fin))
                update_state('production', state.production.to_json())
                if len(state.machines) > 0:
                    assert_facts('machine', [m.to_json() for m in state.machines])
        else:
            rules.init_account()

    def save_state(self):
        try:
            with self.state_file_path.open('w') as fin:
                state = get_state('production')
                del state['$s']
                state = ApplicationState(RawJson(state), self._get_installed_machines())
                json.dump(state.to_json(), fin)
        except Exception:
            os.remove(self.state_file_path)

    def handle_show_status(self):
        machines = self._get_installed_machines()

        machine_description = '\n'.join(str(m) for m in machines)

        storage_description = '\n'.join(str(part_rate) for part_rate in rules.get_storage().iter_part_rates)

        messagebox.showinfo("Status",
                            f'Account balance: {get_state("production")["balance"]}\n'
                            f'Parts in storage:\n{storage_description}\n'
                            f'Machines:\n{machine_description}\n')

    def handle_install_machine(self):
        dialog = DialogInstallMachine(tk.Toplevel(self), rules.production_config.machine_brands)
        machine = dialog.get_results()
        machine.identifier = rules.get_next_machine_id()
        assert_fact('machine', machine.to_json())

    def handle_machine_broke(self):
        machines = self._get_installed_machines()

        if len(machines) == 0:
            messagebox.showinfo('No machines', 'No installed machines found at your business')
            return

        dialog = DialogSelectMachines(tk.Toplevel(self), machines)
        broken_machines = dialog.get_results()

        for machine in broken_machines:
            post('production', {'type': 'machine_loss', 'identifier': machine.identifier})

    def handle_order_parts(self):
        produced_parts = list(rules.production_config.blueprints.keys())
        raw_materials = rules.production_config.raw_materials
        
        dialog = DialogOrderParts(tk.Toplevel(self), produced_parts + raw_materials)

        part_rates = dialog.get_results()
        print(part_rates)

        for part_rate in part_rates:
            post('production', {'type': 'part_request', 'part_rate': part_rate.to_json()})

    @staticmethod
    def _get_installed_machines():
        return [AssignedMachine.from_json(fact) for fact in get_facts('machine') if 'identifier' in fact]
