from dataclasses import dataclass

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable
from json_automatic.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class PartRate(ACompositeJsonSerializable):
    name: str
    rate: float


class PartRateList(list, AContainerJsonSerializable):
    __element_type__ = PartRate
