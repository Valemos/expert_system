import builtins
from copy import deepcopy

import pytest
from durable.lang import *

import rules
from object_types.amounts_dict import AmountsDict
from object_types.machine_properties import AssignedMachine
from object_types.part_rate import PartRate
from rules import production_config, get_next_machine_id
from rules.production_config import machine_types


@pytest.fixture()
def init():
    rules.init_account()


@pytest.fixture(scope="session")
def basic_resources():
    resources = {
        'rubber': 2,
        'aluminum': 4,
        'steel': 10,
    }
    return resources


@pytest.fixture(scope="session")
def start_machines():
    machines = [
        AssignedMachine(get_next_machine_id(), machine_types[0], PartRate('wheel', 1)).to_json(),
        AssignedMachine(get_next_machine_id(), machine_types[0], PartRate('wheel', 1)).to_json(),
        AssignedMachine(get_next_machine_id(), machine_types[2], PartRate('hull', 1)).to_json(),
    ]
    return machines


@pytest.fixture()
def init_facts(init, start_machines, basic_resources):
    retract_facts('machine', get_facts('machine'))
    retract_facts('production', get_facts('production'))
    rules.get_storage().clear()

    assert_facts('machine', list(rules.production_config.machine_brands.values()))
    assert_facts('machine', start_machines)

    for resource in basic_resources.items():
        rules.get_storage().add(PartRate(*resource))

    return start_machines, basic_resources


def test_machine_removed_on_break(init_facts):
    start_machines, basic_resources = init_facts
    machines = [fact for fact in get_facts('machine') if 'identifier' in fact]
    assert builtins.all(machine in machines for machine in start_machines)

    post('production', {'type': 'machine_break', 'identifier': 1})

    assert start_machines[0] not in get_facts('machine')
    assert start_machines[1] in get_facts('machine')
    assert start_machines[2] in get_facts('machine')


def test_target_produce_additional(init_facts):
    parts_initial = deepcopy(rules.get_storage().parts)

    post('production', {'type': 'setup_produce', 'part_rate': PartRate('wheel', 1).to_json()})

    parts_new = rules.get_storage().parts
    difference = parts_new.sub(parts_initial)

    assert difference['wheel'] == 1
    assert difference['rubber'] == -1
    assert difference['aluminum'] == -2

