# src/controller/compressed_air_controller.py

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.validator import compressed_air_validator
from src.config import get_db
from src.repository import compressed_air_repo, all_machine_repo
from src.helper.handler import BaseAppException

import traceback


class CompressedAirController:

    async def get_compressed_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await compressed_air_validator.validate(request)

            return await compressed_air_repo.get_compressed_air(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_COMPRESSED_AIR_ERROR",
                message="Failed to fetch compressed air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_compressed_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await compressed_air_validator.validate(request)

            return await compressed_air_repo.add_compressed_air(
                db=db,
                payload=validated.model_dump()
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_COMPRESSED_AIR_ERROR",
                message="Failed to add compressed air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_compressed_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await compressed_air_validator.validate(request)
            result = await compressed_air_repo.edit_compressed_air(
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
                code="EDIT_COMPRESSED_AIR_ERROR",
                message="Failed to edit compressed air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_compressed_air(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validated = await compressed_air_validator.validate(request)

            return await compressed_air_repo.delete_compressed_air(
                db=db,
                machine_id=validated.machine_id
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_COMPRESSED_AIR_ERROR",
                message="Failed to delete compressed air details",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


compressed_air = CompressedAirController()
