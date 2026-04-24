from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.model.user import User
from src.helper.handler import DatabaseException


class UserRepo:

    async def get_by_email(self, db: AsyncSession, email: str):
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()

        except Exception as error:
            raise DatabaseException(
                message="Failed to fetch user by email",
                payload={
                    "email": email,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
            ) from error


    async def create_user(self, db: AsyncSession, payload: dict):
        try:
            user = User(**payload)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

        except Exception as error:
            raise DatabaseException(
                message="Failed to create user",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
            ) from error


user_repo = UserRepo()