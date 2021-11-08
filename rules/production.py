from durable.lang import *

from object_types.amounts_dict import AmountsDict
from object_types.part_rate import PartRate
from . import production_scheme
from .machine import get_machines_for_part, get_next_machine_id

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
            if 'name' in fact:
                if c.m.identifier == fact['name']:
                    machine_info = fact
                    break

        if machine_info is not None:
            retract_fact('machine', machine_info)
            post('production', {
                'loss': machine_info['cost']
            })
            post('production', {
                'type': 'replace_machine',
                'part_rates': machine_info['produced_parts']
            })

    @when_all(+m.part_rate & (m.type == 'deficiency') & (m.part_rate.amount > 0))
    def handle_deficiencies(c):
        available = get_available_parts()

        post('decision', {'type': 'deficiency', 'part_rate': c.m.part_rate})

    @when_all(+m.part_rate & (m.type == 'buy'))
    def buy_part(c):
        parts_cost = production_scheme.market_prices[c.m.part_rate.identifier] * c.m.part_rate.amount
        if parts_cost > c.s.balance:
            raise ValueError(f'cannot buy {c.m.part_rate}')

        state = get_state('production')
        current_amount = state['parts_storage'].get(c.m.part_rate.identifier, 0)
        state['parts_storage'][c.m.part_rate.identifier] = current_amount + c.m.part_rate.amount
        update_state('production', state)

        post('production', {'loss': parts_cost})

    @when_all(+m.part_rate & (m.type == 'target_produce'))
    def add_component_production(c):
        components = production_scheme.schemes[c.m.part_rate.identifier]
        components = {name: (amount * c.m.part_rate.amount) for name, amount in components.items()}

        machine = get_machines_for_part(c.m.part_rate.identifier)[0]

        for name, amount in components.items():
            post('production', {'type': 'deficiency', 'part_rate': PartRate(name, amount).to_json()})

        assert_fact('machine', {
            'identifier': get_next_machine_id(),
            'brand': machine['brand'],
            'part_rate': c.m.part_rate,
        })


def init_account():
    update_state('production', {'balance': 0, 'parts_storage': {}})


def get_available_parts():
    _parts = AmountsDict()
    for _part in get_state('production')['parts_storage'].items():
        _parts.add(*_part)

    for _fact in get_facts('machine'):
        if 'can_produce' in _fact:
            _parts.add(_fact['can_produce'], _fact['amount'])

    return _parts
