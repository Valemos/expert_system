from dataclasses import dataclass

from types.part_rate import PartRate
from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class MachineProperties(ACompositeJsonSerializable):
    name: str
    cost: float
    produced_parts: list[PartRate]
