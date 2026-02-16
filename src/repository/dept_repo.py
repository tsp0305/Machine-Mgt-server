# src/repository/dept_repo.py
import datetime
import traceback
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Department
from src.helper.handler import BaseAppException


class DeptRepo:

    async def get_dept(self, db: AsyncSession, search: str | None = None):
        try:
            query = select(Department).where(Department.deleted_at == None)

            if search:
                query = query.where(
                    Department.name.ilike(f"%{search}%")
                )

            result = await db.execute(query)
            return result.scalars().all()

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_DEPARTMENT_ERROR",
                message="Failed to fetch departments",
                payload={
                    "search": search,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_dept(self, db: AsyncSession, name: str):
        try:
            query = select(Department).where(Department.name == name)
            old_dept = (await db.execute(query)).scalar_one_or_none()

            if old_dept:
                old_dept.deleted_at = None
                await db.commit()
                await db.refresh(old_dept)
                return old_dept

            dept = Department(name=name)
            db.add(dept)
            await db.commit()
            await db.refresh(dept)
            return dept

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_DEPARTMENT_ERROR",
                message="Failed to add department",
                payload={
                    "name": name,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_dept(self, db: AsyncSession, name: str, id: int):
        try:
            query = select(Department).where(
                Department.id == id,
                Department.deleted_at == None,
            )
            result = await db.execute(query)
            dept = result.scalar_one_or_none()

            if not dept:
                raise BaseAppException(
                    code="DEPARTMENT_NOT_FOUND",
                    message="Department not found",
                    payload={"id": id},
                    status_code=404,
                )

            dept.name = name
            await db.commit()
            await db.refresh(dept)
            return dept

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_DEPARTMENT_ERROR",
                message="Failed to edit department",
                payload={
                    "id": id,
                    "name": name,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_dept(self, db: AsyncSession, id: int):
        try:
            query = select(Department).where(
                Department.id == id,
                Department.deleted_at == None,
            )
            result = await db.execute(query)
            dept = result.scalar_one_or_none()

            if not dept:
                raise BaseAppException(
                    code="DEPARTMENT_NOT_FOUND",
                    message="Department not found for deletion",
                    payload={"id": id},
                    status_code=404,
                )

            dept.deleted_at = datetime.datetime.utcnow()
            await db.commit()
            return {"deleted": True}

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_DEPARTMENT_ERROR",
                message="Failed to delete department",
                payload={
                    "id": id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


dept_repo = DeptRepo()
