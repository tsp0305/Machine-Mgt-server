# src/validator/compressed_air_validator.py
from pydantic import BaseModel
from typing import Optional

from .base_validator import BaseValidator


class compressed_air_validator(BaseValidator, BaseModel):
    id: Optional[int] = None
    machine_id: Optional[int] = None

    nm3_per_hr_per_machine: Optional[float] = None
    nm3_per_hr_total: Optional[float] = None
    pressure_bar: Optional[float] = None
    incoming_hose_size_mm: Optional[float] = None
