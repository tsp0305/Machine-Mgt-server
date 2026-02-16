from .base_validator import BaseValidator
from pydantic import BaseModel

class dept_validator(BaseValidator,BaseModel):
    name :str | None = None
    id:int | None = None
    search:str | None = None
    