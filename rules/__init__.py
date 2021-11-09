from . import production_config
from .production import *
from .machine import *
from .decision import *


for name, machine_info in production_config.machine_brands.items():
    assert_fact('machine', machine_info)

