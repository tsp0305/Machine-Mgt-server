from fastapi import APIRouter
from src.controller import compressed_air

router = APIRouter(
    prefix="/compressed-air",
    tags=["Compressed Air"]
)

router.get("")(compressed_air.get_compressed_air)
router.post("")(compressed_air.add_compressed_air)
router.put("/{id}")(compressed_air.edit_compressed_air)
router.delete("")(compressed_air.delete_compressed_air)
