from typing import List, Optional, Dict
from pydantic import Field
from src.validator.base_validator import BaseValidator


class MachineViewValidator(BaseValidator):
    dept: Optional[List[str]] = None
    machine: Optional[List[str]] = None
    search: Optional[str] = None

    # ✅ NEW (matches frontend exactly)
    description: Optional[Dict[str, List[str]]] = None

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
