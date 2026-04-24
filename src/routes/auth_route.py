from fastapi import APIRouter
from src.controller.auth_controller import auth_controller

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router.post("/signup")(auth_controller.signup)
router.post("/login")(auth_controller.login)
router.post("/refresh")(auth_controller.refresh_token)
router.post("/logout")(auth_controller.logout)