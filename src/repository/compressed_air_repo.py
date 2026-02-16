# src/repository/compressed_air_repo.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from src.model import CompressedAir
from src.helper.handler import BaseAppException


class CompressedAirRepo:

    async def get_compressed_air(self, db: AsyncSession, machine_id: int):
        try:
            query = select(CompressedAir).where(
                CompressedAir.machine_id == machine_id
            )
            result = await db.execute(query)
            compressed_air = result.scalar_one_or_none()

            if not compressed_air:
                raise BaseAppException(
                    code="COMPRESSED_AIR_NOT_FOUND",
                    message="Compressed air details not found for this machine",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            return compressed_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_COMPRESSED_AIR_ERROR",
                message="Failed to fetch compressed air details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_compressed_air(self, db: AsyncSession, payload: dict):
        try:
            compressed_air = CompressedAir(**payload)
            db.add(compressed_air)
            await db.commit()
            await db.refresh(compressed_air)
            return compressed_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_COMPRESSED_AIR_ERROR",
                message="Failed to add compressed air details",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_compressed_air(
        self,
        db: AsyncSession,
        machine_id: int,
        payload: dict,
    ):
        try:
            query = select(CompressedAir).where(
                CompressedAir.machine_id == machine_id
            )
            result = await db.execute(query)
            compressed_air = result.scalar_one_or_none()

            if not compressed_air:
                raise BaseAppException(
                    code="COMPRESSED_AIR_NOT_FOUND",
                    message="Compressed air details not found for update",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            for key, value in payload.items():
                setattr(compressed_air, key, value)

            await db.commit()
            await db.refresh(compressed_air)
            return compressed_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_COMPRESSED_AIR_ERROR",
                message="Failed to update compressed air details",
                payload={
                    "machine_id": machine_id,
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_compressed_air(self, db: AsyncSession, machine_id: int):
        try:
            query = select(CompressedAir).where(
                CompressedAir.machine_id == machine_id
            )
            result = await db.execute(query)
            compressed_air = result.scalar_one_or_none()

            if not compressed_air:
                raise BaseAppException(
                    code="COMPRESSED_AIR_NOT_FOUND",
                    message="Compressed air details not found for deletion",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            await db.delete(compressed_air)
            await db.commit()
            return {"deleted": True}

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_COMPRESSED_AIR_ERROR",
                message="Failed to delete compressed air details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


compressed_air_repo = CompressedAirRepo()
