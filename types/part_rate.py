from dataclasses import dataclass

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class PartRate(ACompositeJsonSerializable):
    name: str
    rate: float
