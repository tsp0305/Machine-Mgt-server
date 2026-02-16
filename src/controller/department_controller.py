from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.validator import dept_validator
from src.config import get_db
from src.repository import dept_repo
from src.helper.handler import BaseAppException

import traceback


class Department:

    async def get_dept(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await dept_validator.validate(request)

            return await dept_repo.get_dept(
                db,
                validated.search
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_DEPARTMENT_ERROR",
                message="Failed to fetch departments",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_dept(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await dept_validator.validate(request)

            return await dept_repo.add_dept(
                db,
                validated.name
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_DEPARTMENT_ERROR",
                message="Failed to add department",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_dept(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await dept_validator.validate(request)

            return await dept_repo.edit_dept(
                db,
                validated.name,
                validated.id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_DEPARTMENT_ERROR",
                message="Failed to edit department",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_dept(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await dept_validator.validate(request)

            return await dept_repo.delete_dept(
                db,
                validated.id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_DEPARTMENT_ERROR",
                message="Failed to delete department",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


dept = Department()
