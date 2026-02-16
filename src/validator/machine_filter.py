from typing import List, Optional
from src.validator.base_validator import BaseValidator


class MachineFilterValidator(BaseValidator):
    dept: Optional[List[str]] = None
    machine: Optional[List[str]] = None
