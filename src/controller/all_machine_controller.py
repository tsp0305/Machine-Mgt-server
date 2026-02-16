from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.validator import MachineFilterValidator, MachineViewValidator
from src.config import get_db
from src.repository.all_machine_repo import all_machine_repo
from src.helper.handler import BaseAppException

import traceback


class AllMachineController:

    async def get_all_machine(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validator = await MachineViewValidator.validate(request)

            return await all_machine_repo.get_all(
                db=db,
                departments=validator.dept,
                machines=validator.machine,
                search=validator.search,
                description=validator.description,  # ✅ NEW
                page=validator.page,
                limit=validator.limit,
            )

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_ALL_MACHINE_ERROR",
                message="Failed to fetch machines",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def refresh(self, db: AsyncSession = Depends(get_db)):
        try:
            return await all_machine_repo.refresh(db=db)

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="REFRESH_MACHINE_MV_ERROR",
                message="Failed to refresh machine materialized view",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def get_specifications(
        self,
        request: Request,
        db: AsyncSession = Depends(get_db)
    ):
        try:
            validator = await MachineFilterValidator.validate(request)

            rows = await all_machine_repo.get_description_specifications(
                db=db,
                departments=validator.dept,
                machines=validator.machine
            )

            description_keys = []
            description_values = {}

            for row in rows:
                key = row["description_key"]
                values = sorted(
                    str(v).strip('"')
                    for v in row["description_values"]
                    if v is not None
                )

                description_keys.append(key)
                description_values[key] = values

            return {
                "descriptionKeys": description_keys,
                "descriptionValues": description_values
            }

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="GET_MACHINE_SPECIFICATIONS_ERROR",
                message="Failed to fetch machine specifications",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


all_machine = AllMachineController()
