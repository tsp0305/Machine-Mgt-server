from fastapi import APIRouter
from src.controller import all_machine

router = APIRouter(
    tags=["Machine View"]
)

router.get("/machine-view")(all_machine.get_all_machine)
router.get("/refresh-mv")(all_machine.refresh)
router.get("/specifications/filters")(all_machine.get_specifications)

