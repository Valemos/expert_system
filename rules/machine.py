from durable.lang import *


with ruleset('machine'):

    @when_all(+m.name & +m.cost & +m.produced_parts)
    def add_new_machine(c):
        print(f'added new machine: {c.m.name} with cost {c.m.cost}u that produces {c.m.produced_parts}')

        for part_rate in c.m.produced_parts:
            assert_fact('machine', {'produce': part_rate['name'], 'machine': c.m.name, 'rate': part_rate['rate']})
