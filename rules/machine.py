from durable.lang import *
from . import production_scheme


with ruleset('machine'):

    @when_all(+m.brand & +m.cost & +m.produced_parts)
    def add_new_machine_brand(c):
        print(f'added machine brand: {c.m.brand} with cost {c.m.cost}u that can produce {c.m.produced_parts}')

        for part_rate in c.m.produced_parts:
            assert_fact('machine', {'can_produce': part_rate['name'], 'machine': c.m.brand, 'rate': part_rate['rate']})

    @when_all(+m.identifier)
    def assign_machine(c):
        print(f'added new machine: {c.m.identifier} ({c.m.brand}) that produces {c.m.part_rate}')


def get_next_machine_id():
    state = get_state('machine')
    cur_id = state.get('last_machine_id', 0)
    next_id = cur_id + 1

    state['last_machine_id'] = next_id
    update_state('machine', state)

    return next_id


def get_machines_for_part(part_name):
    _result_info = []
    for _fact in get_facts('machine'):
        if 'can_produce' in _fact:
            if _fact['can_produce'] == part_name:
                _result_info.append(production_scheme.machines[_fact['machine']])

    return _result_info
