# src/controller/exhaust_air_controller.py

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.validator import exhaust_air_validator
from src.config import get_db
from src.repository import exhaust_air_repo, all_machine_repo
from src.helper.handler import BaseAppException


class ExhaustAirController:

    async def get_exhaust_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await exhaust_air_validator.validate(request)

            return await exhaust_air_repo.get_exhaust_air(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_EXHAUST_AIR_ERROR",
                message="Failed to fetch exhaust air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_exhaust_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await exhaust_air_validator.validate(request)

            result = await exhaust_air_repo.add_exhaust_air(
                db=db,
                payload=validated.model_dump()
            )

            await all_machine_repo.refresh(db)
            return result

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_EXHAUST_AIR_ERROR",
                message="Failed to add exhaust air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_exhaust_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await exhaust_air_validator.validate(request)
            result = await exhaust_air_repo.edit_exhaust_air(
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
                code="EDIT_EXHAUST_AIR_ERROR",
                message="Failed to edit exhaust air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_exhaust_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await exhaust_air_validator.validate(request)

            return await exhaust_air_repo.delete_exhaust_air(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_EXHAUST_AIR_ERROR",
                message="Failed to delete exhaust air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


exhaust_air = ExhaustAirController()
