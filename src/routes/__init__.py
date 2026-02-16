from fastapi import APIRouter

from .dept_routes import router as dept_router
from .machine_routes import router as machine_router
from .electrical_routes import router as electrical_router
from .compressed_air_routes import router as compressed_air_router
from .exhaust_air_routes import router as exhaust_air_router
from .machine_view_routes import router as machine_view_router

router = APIRouter()

router.include_router(dept_router)
router.include_router(machine_router)
router.include_router(electrical_router)
router.include_router(compressed_air_router)
router.include_router(exhaust_air_router)
router.include_router(machine_view_router)
