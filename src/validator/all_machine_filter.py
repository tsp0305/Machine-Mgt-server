# src/validator/machine_validator.py
from pydantic import BaseModel, Field
from typing import Optional
from .base_validator import BaseValidator


class MachineQueryValidator(BaseValidator,BaseModel):
    dept_id: Optional[int] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1)

