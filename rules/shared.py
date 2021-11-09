from object_types.part_storage import PartStorage
from . import production_config


_global_storage = PartStorage()


def get_storage() -> PartStorage:
    global _global_storage
    return _global_storage


_global_part_to_machine_mapping = {}


def get_machines_for_part(part_name):
    global _global_part_to_machine_mapping
    _brand_names = _global_part_to_machine_mapping[part_name]
    return [production_config.machine_brands[brand] for brand in _brand_names]


def add_part_brand_mapping(part_name, brand):
    global _global_part_to_machine_mapping

    machine_list = _global_part_to_machine_mapping.get(part_name, [])
    machine_list.append(brand)
    _global_part_to_machine_mapping[part_name] = machine_list


_global_last_machine_id = 0


def get_next_machine_id():
    global _global_last_machine_id

    _global_last_machine_id += 1
    return _global_last_machine_id
