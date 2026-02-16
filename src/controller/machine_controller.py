# src/controller/machine_controller.py

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.validator import machine_validator,MachineQueryValidator
from src.config import get_db
from src.repository import machine_repo, all_machine_repo
from src.helper.handler import BaseAppException


class MachineController:

    async def get_machine(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await MachineQueryValidator.validate(request)

            return await machine_repo.get_machine(
                db=db,
                dept_id=validated.dept_id,
                search=validated.search,
                page=validated.page,
                limit=validated.limit
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_MACHINE_ERROR",
                message="Failed to fetch machines",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_machine(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await machine_validator.validate(request)

            return await machine_repo.add_machine(
                db=db,
                payload=validated.model_dump()
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_MACHINE_ERROR",
                message="Failed to add machine",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_machine(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await machine_validator.validate(request)
            result = await machine_repo.edit_machine(
                db=db,
                machine_id=validated.id,
                payload=validated.model_dump()
            )

            await all_machine_repo.refresh(db)
            return result

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_MACHINE_ERROR",
                message="Failed to edit machine",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_machine(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await machine_validator.validate(request)

            result = await machine_repo.delete_machine(
                db=db,
                machine_id=validated.id
            )

            await all_machine_repo.refresh(db)
            return result

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_MACHINE_ERROR",
                message="Failed to delete machine",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


machine = MachineController()
