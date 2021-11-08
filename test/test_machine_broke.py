import pytest
from durable.lang import *

import rules
from object_types.machine_properties import AssignedMachine
from object_types.part_rate import PartRate
from rules import get_available_parts
from rules.production_scheme import machine_types


@pytest.fixture()
def init():
    rules.init_account()


@pytest.fixture()
def basic_resources(init):
    resources = {
        'rubber': 2,
        'aluminum': 4,
    }
    cur_state = get_state('production')
    cur_state['parts_storage'] = resources
    update_state('production', cur_state)

    return resources


@pytest.fixture()
def start_machines(basic_resources):
    machines = [
        AssignedMachine(1, machine_types[0], PartRate('wheel', 1)).to_json(),
        AssignedMachine(2, machine_types[2], PartRate('hull', 1)).to_json(),
        AssignedMachine(3, machine_types[0], PartRate('wheel', 1)).to_json(),
    ]
    assert_facts('machine', machines)

    return machines


def test_machine_removed(start_machines):
    assert all(machine == fact for machine, fact in zip(start_machines, get_facts('machine')))

    post('production', {'type': 'machine_break', 'name': '1'})

    assert start_machines[0] not in get_facts('machine')
    assert start_machines[1] in get_facts('machine')
    assert start_machines[2] in get_facts('machine')


def test_target_produce_additional(start_machines):
    parts_initial = get_available_parts()
    post('production', {'type': 'target_produce', 'part_rate': PartRate('wheel', 1)})
    parts_new = get_available_parts()

    assert parts_new.sub(parts_initial)['wheel'] == 1

