# src/repository/machine_repo.py
import traceback
from sqlalchemy import select,func,or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Machine
from src.helper.handler import BaseAppException


class MachineRepo:

    async def get_machine(
        self,
        db: AsyncSession,
        dept_id: int | None = None,
        search: str | None = None,
        page: int | None = None,
        limit: int | None = None
    ):
        try:
            query = select(Machine)
            if dept_id:
                query = query.where(Machine.dept_id == dept_id)
            if search:
                query = query.where(
                    or_(
                        Machine.model_name.ilike(f"%{search}%"),
                        Machine.model.ilike(f"%{search}%")
                    )
                )

            # If pagination parameters are provided, return paginated response
            if page is not None and limit is not None:
                # 1️⃣ Count total items
                count_query = select(func.count()).select_from(query.subquery())
                total_result = await db.execute(count_query)
                total_items = total_result.scalar_one()

                # 2️⃣ Apply pagination
                offset = (page - 1) * limit
                query = query.offset(offset).limit(limit)

                result = await db.execute(query)
                machines = result.scalars().all()

                total_pages = (total_items + limit - 1) // limit  

                return {
                    "data": machines,
                    "pagination": {
                        "currentPage": page,
                        "itemsPerPage": limit,
                        "totalItems": total_items,
                        "totalPages": total_pages,
                    },
                }
            
            # If no pagination parameters, return all results without pagination
            else:
                result = await db.execute(query)
                machines = result.scalars().all()
                
                return {
                    "data": machines,
                    "pagination": None,
                }

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_MACHINES_ERROR",
                message="Failed to fetch machines",
                payload={
                    "dept_id": dept_id,
                    "search": search,
                    "page": page,
                    "limit": limit,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


    async def get_machine_by_id(self, db: AsyncSession, machine_id: int):
        try:
            query = select(Machine).where(Machine.id == machine_id)
            result = await db.execute(query)
            machine = result.scalar_one_or_none()

            if not machine:
                raise BaseAppException(
                    code="MACHINE_NOT_FOUND",
                    message="Machine not found",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            return machine

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_MACHINE_ERROR",
                message="Failed to fetch machine",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def add_machine(self, db: AsyncSession, payload: dict):
        try:
            machine = Machine(**payload)
            db.add(machine)
            await db.commit()
            await db.refresh(machine)
            return machine

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="ADD_MACHINE_ERROR",
                message="Failed to add machine",
                payload={
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def edit_machine(self, db: AsyncSession, machine_id: int, payload: dict):
        try:
            query = select(Machine).where(Machine.id == machine_id)
            result = await db.execute(query)
            machine = result.scalar_one_or_none()

            if not machine:
                raise BaseAppException(
                    code="MACHINE_NOT_FOUND",
                    message="Machine not found for update",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            for key, value in payload.items():
                setattr(machine, key, value)

            await db.commit()
            await db.refresh(machine)
            return machine

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="EDIT_MACHINE_ERROR",
                message="Failed to edit machine",
                payload={
                    "machine_id": machine_id,
                    "payload": payload,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def delete_machine(self, db: AsyncSession, machine_id: int):
        try:
            query = select(Machine).where(Machine.id == machine_id)
            result = await db.execute(query)
            machine = result.scalar_one_or_none()

            if not machine:
                raise BaseAppException(
                    code="MACHINE_NOT_FOUND",
                    message="Machine not found for deletion",
                    payload={"machine_id": machine_id},
                    status_code=404,
                )

            await db.delete(machine)
            await db.commit()
            return {"deleted": True}

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="DELETE_MACHINE_ERROR",
                message="Failed to delete machine",
                payload={
                    "machine_id": machine_id,
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


machine_repo = MachineRepo()
