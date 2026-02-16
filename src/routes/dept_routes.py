from fastapi import APIRouter
from src.controller import dept

router = APIRouter(
    prefix="/dept",
    tags=["Department"]
)

router.get("")(dept.get_dept)
router.post("")(dept.add_dept)
router.put("")(dept.edit_dept)
router.delete("")(dept.delete_dept)
