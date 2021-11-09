from object_types.machine_properties import MachineProperties
from object_types.part_rate import PartRate


def map_to_dict(*ls, **kw):
    return {e[kw['key']]: e for e in ls}


blueprints = {
    'car': {'wheel': 4, 'hull': 1, 'engine': 1},
    'wheel': {'aluminum': 2, 'rubber': 1},
    'hull': {'steel': 10},
    'engine': {'steel': 3, 'aluminum': 1}
}

machine_brands = map_to_dict(
    MachineProperties(
        'Tormach',
        200,
        [
            PartRate('wheel', 10),
            PartRate('hull', 1),
        ],
        True
    ).to_json(),
    MachineProperties(
        'Powermatic',
        400,
        [
            PartRate('wheel', 5),
            PartRate('engine', 10),
        ],
        False
    ).to_json(),
    MachineProperties(
        'Industrial robot',
        700,
        [
            PartRate('car', 1),
            PartRate('wheel', 1),
            PartRate('hull', 1),
        ],
        False
    ).to_json(),
    key='brand'
)

machine_types = list(machine_brands.keys())

market_prices = {
    'rubber': 1,
    'aluminum': 3,
    'steel': 2,
    'wheel': 10,
    'hull': 50,
    'engine': 40,
}
