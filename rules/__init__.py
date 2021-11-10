from . import production_config
from .production import *
from .machine import *
from .decision import *


for machine_info in production_config.machine_brands_dict.values():
    assert_fact('machine', machine_info)

