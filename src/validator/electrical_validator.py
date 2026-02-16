# src/validator/electrical_validator.py
from pydantic import BaseModel
from typing import Optional

from .base_validator import BaseValidator


class electrical_validator(BaseValidator, BaseModel):
    id: Optional[int] = None
    machine_id: Optional[int] = None

    installed_power_kw_per_machine: Optional[float] = None
    installed_power_kw_total: Optional[float] = None
    fuse_or_mccb: Optional[int] = None
    power_cable_size_sqmm: Optional[str] = None
    earth_wire_size_sqmm: Optional[str] = None
