# src/repository/exhaust_air_repo.py
import traceback
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import ExhaustAir
from src.helper.handler import BaseAppException


class ExhaustAirRepo:

    async def get_exhaust_air(self, db: AsyncSession, machine_id: int):
        try:
            query = select(ExhaustAir).where(ExhaustAir.machine_id == machine_id)
            result = await db.execute(query)
            exhaust_air = result.scalar_one_or_none()

            if not exhaust_air:
                raise BaseAppException(
                    code="EXHAUST_AIR_NOT_FOUND",
                    message="Exhaust air details not found",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            return exhaust_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_EXHAUST_AIR_ERROR",
                message="Failed to fetch exhaust air details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_exhaust_air(self, db: AsyncSession, payload: dict):
        try:
            exhaust_air = ExhaustAir(**payload)
            db.add(exhaust_air)
            await db.commit()
            await db.refresh(exhaust_air)
            return exhaust_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_EXHAUST_AIR_ERROR",
                message="Failed to add exhaust air details",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_exhaust_air(self, db: AsyncSession, machine_id: int, payload: dict):
        try:
            query = select(ExhaustAir).where(ExhaustAir.machine_id == machine_id)
            result = await db.execute(query)
            exhaust_air = result.scalar_one_or_none()

            if not exhaust_air:
                raise BaseAppException(
                    code="EXHAUST_AIR_NOT_FOUND",
                    message="Exhaust air details not found for update",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            for key, value in payload.items():
                setattr(exhaust_air, key, value)

            await db.commit()
            await db.refresh(exhaust_air)
            return exhaust_air

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_EXHAUST_AIR_ERROR",
                message="Failed to edit exhaust air details",
                payload={
                    "machine_id": machine_id,
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_exhaust_air(self, db: AsyncSession, machine_id: int):
        try:
            query = select(ExhaustAir).where(ExhaustAir.machine_id == machine_id)
            result = await db.execute(query)
            exhaust_air = result.scalar_one_or_none()

            if not exhaust_air:
                raise BaseAppException(
                    code="EXHAUST_AIR_NOT_FOUND",
                    message="Exhaust air details not found for deletion",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            await db.delete(exhaust_air)
            await db.commit()
            return {"deleted": True}

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_EXHAUST_AIR_ERROR",
                message="Failed to delete exhaust air details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


exhaust_air_repo = ExhaustAirRepo()
