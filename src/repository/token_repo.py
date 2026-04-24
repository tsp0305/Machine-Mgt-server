from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import traceback
from datetime import datetime, timedelta, timezone  
from src.model.refresh_token import RefreshToken
from src.helper.handler import DatabaseException
from settings import settings

class TokenRepo:
    async def create_token(self, db: AsyncSession, payload: dict):
        try:
            if "expires_at" not in payload:
                payload["expires_at"] = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            token = RefreshToken(**payload)
            db.add(token)
            await db.commit()
            await db.refresh(token)
            return token

        except Exception as error:
            raise DatabaseException(
                message="Failed to create refresh token",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
            ) from error


    async def get_token(self, db: AsyncSession, token: str):
        try:
            result = await db.execute(
                select(RefreshToken).where(
                    RefreshToken.token == token
                )
            )
            return result.scalar_one_or_none()

        except Exception as error:
            raise DatabaseException(
                message="Failed to fetch refresh token",
                payload={
                    "token": token,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
            ) from error


    async def delete_token(self, db: AsyncSession, token: str):
        try:
            await db.execute(
                delete(RefreshToken).where(
                    RefreshToken.token == token
                )
            )
            await db.commit()

        except Exception as error:
            raise DatabaseException(
                message="Failed to delete refresh token",
                payload={
                    "token": token,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
            ) from error


token_repo = TokenRepo()