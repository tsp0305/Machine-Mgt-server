from fastapi import APIRouter
from src.controller import machine

router = APIRouter(
    prefix="/machine",
    tags=["Machine"]
)

router.get("")(machine.get_machine)
router.get("/{id}")(machine.get_machine)
router.post("")(machine.add_machine)
router.put("/{id}")(machine.edit_machine)
router.delete("")(machine.delete_machine)
