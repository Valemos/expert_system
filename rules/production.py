from durable.lang import *

from object_types.part_rate import PartRate
from . import production_config
from .shared import get_storage, get_decisions


def init_account():
    update_state('production', {'balance': 0})


with ruleset('production'):

    @when_all(+m.loss)
    def try_compensate_loss(c):
        get_decisions().compensate_loss(c.m.loss)
        c.s.balance -= c.m.loss

    @when_all(+m.income)
    def add_income(c):
        c.s.balance += c.m.income

    @when_all(+m.identifier & (m.type == 'machine_loss'))
    def machine_remove(c):
        machine_info = None
        for fact in get_facts('machine'):
            if 'identifier' in fact:
                if c.m.identifier == fact['identifier']:
                    machine_info = fact
                    break

        print(f'remove machine {machine_info}')

        if machine_info is not None:
            produced_part_name = machine_info['part_rate']['name']
            get_storage().take(machine_info['part_rate'])
            for component, amount in production_config.blueprints[produced_part_name].items():
                get_storage().add(PartRate(component, amount))

            retract_fact('machine', machine_info)
            cost = production_config.machine_brands_dict[machine_info['brand']]['cost']

            get_decisions().compensate_loss(cost)
            get_decisions().deficiency(PartRate.from_json(machine_info['part_rate']))

    @when_all(+m.part_rate & (m.type == 'part_request'))
    def part_request(c):
        in_storage_amount = get_storage()[c.m.part_rate.name]

        get_storage().take(c.m.part_rate)

        if in_storage_amount < c.m.part_rate.amount:
            additional_amount = c.m.part_rate.amount - in_storage_amount
            additional_rate = PartRate(c.m.part_rate.name, additional_amount)
            get_decisions().deficiency(additional_rate)

    @when_all(+m.part_rate & (m.type == 'buy'))
    def buy_part(c):
        parts_cost = production_config.market_prices[c.m.part_rate.name] * c.m.part_rate.amount
        get_storage().add(c.m.part_rate)
        post('production', {'loss': parts_cost})
