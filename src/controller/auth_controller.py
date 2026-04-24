from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.validator.auth_validator import (
    SignupValidator,
    LoginValidator,
    RefreshRequest,
    LogoutRequest
)

from src.repository.user_repo import user_repo
from src.repository.token_repo import token_repo

from src.helper.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)

from src.config import get_db
from src.helper.handler import BaseAppException


class AuthController:

    async def signup(self, request: Request, db: AsyncSession = Depends(get_db)):
        try:

            validated = await SignupValidator.validate(request)

            existing = await user_repo.get_by_email(db, validated.email)

            if existing:
                raise BaseAppException(
                    code="USER_ALREADY_EXISTS",
                    message="Email already registered",
                    payload={"email": validated.email},
                    status_code=400
                )

            user = await user_repo.create_user(
                db=db,
                payload={
                    "email": validated.email,
                    "password_hash": hash_password(validated.password),
                    "role": "user"
                }
            )

            access = create_access_token({
                "sub": str(user.id),
                "role": user.role,
                "email": user.email
            })

            refresh = create_refresh_token({"sub": str(user.id), "role": user.role, "email": user.email})

            await token_repo.create_token(
                db,
                {
                    "user_id": user.id,
                    "token": refresh
                }
            )

            return {
                "access_token": access,
                "refresh_token": refresh,
                "token_type": "bearer"
            }

        except (BaseAppException, HTTPException):
            raise

        except Exception as error:
            raise BaseAppException(
                code="SIGNUP_ERROR",
                message="Signup failed",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500
            ) from error


    async def login(self, request: Request, db: AsyncSession = Depends(get_db)):
        try:

            validated = await LoginValidator.validate(request)

            user = await user_repo.get_by_email(db, validated.email)

            if not user or not verify_password(
                validated.password,
                user.password_hash
            ):
                raise BaseAppException(
                    code="INVALID_CREDENTIALS",
                    message="Invalid email or password",
                    status_code=401
                )

            access = create_access_token({
                "sub": str(user.id),
                "role": user.role,
                "email": user.email
            })

            refresh = create_refresh_token({"sub": str(user.id), "role": user.role, "email": user.email})

            await token_repo.create_token(
                db,
                {
                    "user_id": user.id,
                    "token": refresh
                }
            )

            return {
                "access_token": access,
                "refresh_token": refresh,
                "token_type": "bearer"
            }

        except (BaseAppException, HTTPException):
            raise

        except Exception as error:
            raise BaseAppException(
                code="LOGIN_ERROR",
                message="Login failed",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500
            ) from error


    async def refresh_token(self, request: Request, db: AsyncSession = Depends(get_db)):
        try:

            validated = await RefreshRequest.validate(request)

            payload = verify_token(validated.refresh_token)

            token = await token_repo.get_token(db, validated.refresh_token)

            if not token:
                raise BaseAppException(
                    code="INVALID_REFRESH",
                    message="Refresh token invalid",
                    status_code=401
                )

            access = create_access_token({
                "sub": payload["sub"], 
                "role": payload.get("role", "user"),
                "email": payload.get("email", "")
            })


            return {
                "access_token": access
            }

        except (BaseAppException, HTTPException):
            raise

        except Exception as error:
            raise BaseAppException(
                code="REFRESH_ERROR",
                message="Token refresh failed",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500
            ) from error


    async def logout(self, request: Request, db: AsyncSession = Depends(get_db)):
        try:

            validated = await LogoutRequest.validate(request)

            await token_repo.delete_token(
                db,
                validated.refresh_token
            )

            return {"message": "Logged out successfully"}

        except (BaseAppException, HTTPException):
            raise

        except Exception as error:
            raise BaseAppException(
                code="LOGOUT_ERROR",
                message="Logout failed",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500
            ) from error


auth_controller = AuthController()