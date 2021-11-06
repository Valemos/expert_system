from durable.lang import *


with ruleset('machine_break'):

    @when_all(+m.name)
    def machine_remove(c):
        machine_info = None
        for fact in get_facts('machine'):
            if 'name' in fact:
                if c.m.name == fact['name']:
                    machine_info = fact

        if machine_info is not None:
            retract_fact('machine', machine_info)
            assert_fact('account', {
                'loss': machine_info['cost']
            })
            assert_fact('machine_break', {
                'action': 'replace_machine',
                'part_rates': machine_info['produced_parts']
            })

