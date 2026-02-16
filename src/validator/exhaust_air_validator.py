# src/validator/exhaust_air_validator.py

from pydantic import BaseModel
from typing import Optional
from .base_validator import BaseValidator


class exhaust_air_validator(BaseValidator, BaseModel):
    id: Optional[int] = None
    machine_id: Optional[int] = None

    air_m3_sec_per_machine: Optional[float] = None
    air_m3_sec_total: Optional[float] = None

    air_to_trench_per_machine: Optional[float] = None
    air_to_trench_total: Optional[float] = None

    air_to_filter_per_machine: Optional[float] = None
    air_to_filter_total: Optional[float] = None

    pressure_pascal: Optional[float] = None
    remarks: Optional[str] = None
