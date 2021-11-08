from dataclasses import dataclass

from object_types.part_rate import PartRate
from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class MachineProperties(ACompositeJsonSerializable):
    brand: str
    cost: float
    produced_parts: list[PartRate]
    needs_staff: bool


@dataclass
class AssignedMachine(ACompositeJsonSerializable):
    identifier: int
    brand: str
    part_rate: PartRate
