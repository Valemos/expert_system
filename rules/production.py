from durable.lang import *

from object_types.part_rate import PartRate
from . import production_config
from .shared import get_machines_for_part, get_next_machine_id, get_storage


def init_account():
    update_state('production', {'balance': 0})


with ruleset('production'):

    @when_all(+m.loss)
    def try_compensate_loss(c):
        assert_fact('decision', {'type': 'compensate_loss', 'amount': c.m.loss})
        c.s.balance -= c.m.loss

    @when_all(+m.income)
    def add_income(c):
        c.s.balance += c.m.income

    @when_all(+m.identifier & (m.type == 'machine_break'))
    def machine_remove(c):
        machine_info = None
        for fact in get_facts('machine'):
            if 'identifier' in fact:
                if c.m.identifier == fact['identifier']:
                    machine_info = fact
                    break

        if machine_info is not None:
            produced_name = machine_info['part_rate']['name']
            for component, amount in production_config.blueprints[produced_name].items():
                get_storage().add(PartRate(component, amount))

            retract_fact('machine', machine_info)
            brand = machine_info['brand']
            post('production', {
                'loss': production_config.machine_brands[brand]['cost']
            })
            post('decision', {
                'type': 'replace_machine',
                'part_rate': machine_info['part_rate']
            })

    @when_all(+m.part_rate & (m.type == 'part_request'))
    def part_request(c):
        in_storage_amount = get_storage()[c.m.part_rate.name]

        get_storage().take(c.m.part_rate)

        if in_storage_amount < c.m.part_rate.amount:
            additional_amount = in_storage_amount - c.m.part_rate.amount
            additional_rate = PartRate(c.m.part_rate.name, additional_amount).to_json()
            post('decision', {'type': 'deficiency', 'part_rate': additional_rate})


    @when_all(+m.part_rate & (m.type == 'buy'))
    def buy_part(c):
        parts_cost = production_config.market_prices[c.m.part_rate.name] * c.m.part_rate.amount
        if parts_cost > c.s.balance:
            raise ValueError(f'cannot buy {c.m.part_rate}')

        get_storage().add(c.m.part_rate)
        post('production', {'loss': parts_cost})

    @when_all(+m.part_rate & (m.type == 'setup_produce'))
    def add_component_production(c):
        components = production_config.blueprints[c.m.part_rate.name]
        components = {name: (amount * c.m.part_rate.amount) for name, amount in components.items()}

        for name, amount in components.items():
            post('production', {'type': 'part_request', 'part_rate': PartRate(name, amount).to_json()})

        machine = get_machines_for_part(c.m.part_rate.name)[0]

        assert_fact('machine', {
            'identifier': get_next_machine_id(),
            'brand': machine['brand'],
            'part_rate': PartRate(c.m.part_rate.name, c.m.part_rate.amount).to_json(),
        })
