from pydantic import BaseModel
from typing import Optional, Dict, Any

from .base_validator import BaseValidator


class machine_validator(BaseValidator, BaseModel):
    id: Optional[int] = None
    model_name: Optional[str] = None
    description: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    waste_collection_split: Optional[str] = None
    can_changer_type: Optional[str] = None
    feed_type: Optional[str] = None
    wcs_type: Optional[str] = None
    webdoff_type: Optional[str] = None
    product_code: Optional[int] = None
    quantity: Optional[int] = None
    weight_kg: Optional[float] = None
    dept_id: Optional[int] = None
