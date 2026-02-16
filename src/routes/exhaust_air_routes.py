from fastapi import APIRouter
from src.controller import exhaust_air

router = APIRouter(
    prefix="/exhaust-air",
    tags=["Exhaust Air"]
)

router.get("")(exhaust_air.get_exhaust_air)
router.post("")(exhaust_air.add_exhaust_air)
router.put("/{id}")(exhaust_air.edit_exhaust_air)
router.delete("")(exhaust_air.delete_exhaust_air)
