from dataclasses import dataclass

from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable

from object_types.part_rate import PartRate


@dataclass
class AssignedMachine(ACompositeJsonSerializable):
    identifier: int = 0
    brand: str = ''
    part_rate: PartRate = PartRate()

    def __str__(self):
        return f'{self.brand} {self.identifier}: {str(self.part_rate)}'
