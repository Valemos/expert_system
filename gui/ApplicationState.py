from dataclasses import dataclass, field

from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable
from json_annotated.raw_json import RawJson

from object_types.assigned_machine import AssignedMachine


@dataclass
class ApplicationState(ACompositeJsonSerializable):
    production: RawJson = field(default_factory=RawJson)
    machines: list[AssignedMachine] = field(default_factory=list)
