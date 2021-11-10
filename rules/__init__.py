from . import production_config
from .shared import *
from .production import *
from .machine import *


for machine_info in production_config.machine_brands_dict.values():
    assert_fact('machine', machine_info)

