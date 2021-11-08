from .machine import *
from .production import *
from .decision import *
from . import production_scheme


for name, machine_info in production_scheme.machines.items():
    assert_fact('machine', machine_info)
