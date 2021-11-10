from durable.lang import *

from object_types.part_rate import PartRate
from . import production_config
from .shared import get_storage, add_part_brand_mapping


with ruleset('machine'):

    @when_all(+m.brand & +m.cost & +m.produced_parts)
    def add_new_machine_brand(c):
        print(f'added machine brand: {c.m.brand} with cost {c.m.cost}u that can produce {c.m.produced_parts}')

        for part_rate in c.m.produced_parts:
            assert_fact('machine', {'brand': c.m.brand, 'can_produce': part_rate})

    @when_all(+m.identifier)
    def assign_machine(c):
        print(f'added new machine: {c.m.identifier} ({c.m.brand}) that produces {c.m.part_rate}')

        blueprint = production_config.blueprints.get(c.m.part_rate.name, None)
        if blueprint is None:
            raise ValueError('no blueprint for produced object')

        post('production', {'loss': production_config.machine_brands_dict[c.m.brand]['cost']})
        get_storage().add(c.m.part_rate)
        
        components = production_config.blueprints[c.m.part_rate.name]
        components = {name: (amount * c.m.part_rate.amount) for name, amount in components.items()}

        for name, amount in components.items():
            post('production', {'type': 'part_request', 'part_rate': PartRate(name, amount).to_json()})


    @when_all(+m.can_produce & +m.brand)
    def add_can_produce(c):
        add_part_brand_mapping(c.m.can_produce.name, c.m.brand)
