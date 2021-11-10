from typing import Iterator

from object_types.amounts_dict import AmountsDict
from object_types.part_rate import PartRate


def part_rate_conversion(function):
    def wrapper(self, part_rate):
        if isinstance(part_rate, dict):
            return function(self, PartRate.from_json(part_rate))
        else:
            return function(self, part_rate)
    return wrapper


class PartStorage:

    def __init__(self):
        self._parts = AmountsDict()

    def __getitem__(self, item):
        if item in self._parts:
            return self._parts[item]
        else:
            return 0

    @property
    def parts(self):
        return self._parts

    @property
    def iter_part_rates(self) -> Iterator[PartRate]:
        return (PartRate(part, amount) for part, amount in self._parts)

    @part_rate_conversion
    def add(self, part_rate: PartRate):
        self._parts.add(part_rate.name, part_rate.amount)

    @part_rate_conversion
    def take(self, part_rate: PartRate):
        self._parts.add(part_rate.name, -part_rate.amount)

    def clear(self):
        self._parts = AmountsDict()
