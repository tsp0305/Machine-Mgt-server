# src/controller/electrical_controller.py

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.validator import electrical_validator
from src.config import get_db
from src.repository import electrical_repo, all_machine_repo
from src.helper.handler import BaseAppException


class ElectricalController:

    async def get_electrical(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await electrical_validator.validate(request)

            return await electrical_repo.get_electrical(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_ELECTRICAL_ERROR",
                message="Failed to fetch electrical details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_electrical(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await electrical_validator.validate(request)

            return await electrical_repo.add_electrical(
                db=db,
                payload=validated.model_dump()
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_ELECTRICAL_ERROR",
                message="Failed to add electrical details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_electrical(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await electrical_validator.validate(request)
            print(validated)
            result = await electrical_repo.edit_electrical(
                db=db,
                machine_id=validated.machine_id,
                payload=validated.model_dump()
            )

            await all_machine_repo.refresh(db)
            return result

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_ELECTRICAL_ERROR",
                message="Failed to edit electrical details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_electrical(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await electrical_validator.validate(request)

            return await electrical_repo.delete_electrical(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_ELECTRICAL_ERROR",
                message="Failed to delete electrical details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


electrical = ElectricalController()
