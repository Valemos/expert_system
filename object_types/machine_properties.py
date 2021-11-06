from dataclasses import dataclass

from object_types.part_rate import PartRateList
from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class MachineProperties(ACompositeJsonSerializable):
    name: str
    cost: float
    produced_parts: PartRateList
