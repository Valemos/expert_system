import pytest
from durable.lang import *

import rules
from object_types.machine_properties import MachineProperties
from object_types.part_rate import PartRate, PartRateList


@pytest.fixture()
def start_machines():
    machines = [
        MachineProperties('1', 100, PartRateList([PartRate('part1', 1)])).to_json(),
        MachineProperties('2', 400, PartRateList([PartRate('part2', 1)])).to_json(),
        MachineProperties('3', 100, PartRateList([PartRate('part1', 1)])).to_json(),
    ]
    assert_facts('machine', machines)
    return machines


def test_machine_removed(start_machines):
    assert all(machine == fact for machine, fact in zip(start_machines, get_facts('machine')))

    assert_fact('machine_break', {'name': '1'})

    assert start_machines[0] not in get_facts('machine')
    assert start_machines[1] in get_facts('machine')
    assert start_machines[2] in get_facts('machine')
