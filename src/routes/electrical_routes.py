from fastapi import APIRouter
from src.controller import electrical

router = APIRouter(
    prefix="/electrical",
    tags=["Electrical"]
)

router.get("")(electrical.get_electrical)
router.post("")(electrical.add_electrical)
router.put("/{id}")(electrical.edit_electrical)
router.delete("")(electrical.delete_electrical)
