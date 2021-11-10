from dataclasses import dataclass

from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class PartRate(ACompositeJsonSerializable):
    name: str = ''
    amount: float = 0

    def __str__(self):
        return f'{self.name} x {self.amount}'
