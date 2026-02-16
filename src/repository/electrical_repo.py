# src/repository/electrical_repo.py
import traceback
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Electrical
from src.helper.handler import BaseAppException


class ElectricalRepo:

    async def get_electrical(self, db: AsyncSession, machine_id: int):
        try:
            query = select(Electrical).where(Electrical.machine_id == machine_id)
            result = await db.execute(query)
            electrical = result.scalar_one_or_none()

            if not electrical:
                raise BaseAppException(
                    code="ELECTRICAL_NOT_FOUND",
                    message="Electrical details not found",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            return electrical

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_ELECTRICAL_ERROR",
                message="Failed to fetch electrical details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_electrical(self, db: AsyncSession, payload: dict):
        try:
            electrical = Electrical(**payload)
            db.add(electrical)
            await db.commit()
            await db.refresh(electrical)
            return electrical

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_ELECTRICAL_ERROR",
                message="Failed to add electrical details",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_electrical(self, db: AsyncSession, machine_id: int, payload: dict):
        try:
            query = select(Electrical).where(Electrical.machine_id == machine_id)
            result = await db.execute(query)
            electrical = result.scalar_one_or_none()

            if not electrical:
                raise BaseAppException(
                    code="ELECTRICAL_NOT_FOUND",
                    message="Electrical details not found for update",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            for key, value in payload.items():
                setattr(electrical, key, value)

            await db.commit()
            await db.refresh(electrical)
            return electrical

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_ELECTRICAL_ERROR",
                message="Failed to edit electrical details",
                payload={
                    "machine_id": machine_id,
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_electrical(self, db: AsyncSession, machine_id: int):
        try:
            query = select(Electrical).where(Electrical.machine_id == machine_id)
            result = await db.execute(query)
            electrical = result.scalar_one_or_none()

            if not electrical:
                raise BaseAppException(
                    code="ELECTRICAL_NOT_FOUND",
                    message="Electrical details not found for deletion",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            await db.delete(electrical)
            await db.commit()
            return {"deleted": True}

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_ELECTRICAL_ERROR",
                message="Failed to delete electrical details",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


electrical_repo = ElectricalRepo()
