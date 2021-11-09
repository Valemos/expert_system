from dataclasses import dataclass

from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class PartRate(ACompositeJsonSerializable):
    name: str
    amount: float
