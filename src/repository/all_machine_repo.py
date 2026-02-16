# src/repository/all_machine_repo.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import math
import traceback
from src.helper.handler import BaseAppException


class AllMachineRepo:

    async def get_all(
        self,
        db: AsyncSession,
        departments: list[str] | None = None,
        machines: list[str] | None = None,
        search: str | None = None,
        description: dict[str, list[str]] | None = None,  # ✅ NEW
        page: int = 1,
        limit: int = 10,
    ):
        try:
            conditions = []
            params = {}

            # 🏢 department filter
            if departments:
                conditions.append("department_name = ANY(:departments)")
                params["departments"] = departments

            # 🏭 machine filter
            if machines:
                conditions.append("model_name = ANY(:machines)")
                params["machines"] = machines

            # 🔍 search
            if search:
                conditions.append("""
                    (
                        LOWER(model_name) LIKE :search OR
                        LOWER(model) LIKE :search OR
                        LOWER(department_name) LIKE :search OR
                        CAST(product_code AS TEXT) LIKE :search
                    )
                """)
                params["search"] = f"%{search.lower()}%"

            # 🔥 JSONB DYNAMIC FILTERS (CORRECT WAY)
            if description:
                for i, (key, values) in enumerate(description.items()):
                    if not values:
                        continue

                    conditions.append(
                        f"""
                        description ->> :key_{i} = ANY(:values_{i})
                        """
                    )
                    params[f"key_{i}"] = key
                    params[f"values_{i}"] = values

            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            # ---------- COUNT ----------
            count_query = text(f"""
                SELECT COUNT(*)
                FROM machine_full_view
                {where_clause}
            """)
            total_items = (await db.execute(count_query, params)).scalar() or 0

            total_pages = math.ceil(total_items / limit)
            offset = (page - 1) * limit

            # ---------- DATA ----------
            params["limit"] = limit
            params["offset"] = offset

            data_query = text(f"""
                SELECT *
                FROM machine_full_view
                {where_clause}
                ORDER BY machine_id
                LIMIT :limit OFFSET :offset
            """)

            rows = (await db.execute(data_query, params)).mappings().all()

            return {
                "data": [dict(row) for row in rows],
                "pagination": {
                    "currentPage": page,
                    "totalPages": total_pages,
                    "totalItems": total_items,
                    "itemsPerPage": limit,
                },
            }
        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_ALL_MACHINES_ERROR",
                message="Failed to fetch machines",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def refresh(self, db: AsyncSession):
        try:
            await db.execute(
                text("REFRESH MATERIALIZED VIEW CONCURRENTLY machine_full_view")
            )
            await db.commit()

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="REFRESH_MACHINE_VIEW_ERROR",
                message="Failed to refresh machine materialized view",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error

    async def get_description_specifications(
        self,
        db: AsyncSession,
        departments: list[str] | None = None,
        machines: list[str] | None = None,
    ):
        try:
            conditions = []
            params = {}

            if departments:
                conditions.append("department_name = ANY(:departments)")
                params["departments"] = departments

            if machines:
                conditions.append("model_name = ANY(:machines)")
                params["machines"] = machines

            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            query = text(f"""
                SELECT
                    key AS description_key,
                    ARRAY_AGG(DISTINCT value::text) AS description_values
                FROM machine_full_view,
                     jsonb_each(description::jsonb)
                {where_clause}
                GROUP BY key
                ORDER BY key
            """)

            result = await db.execute(query, params)
            return result.mappings().all()

        except BaseAppException:
            raise

        except Exception as error:
            raise BaseAppException(
                code="FETCH_MACHINE_SPECIFICATIONS_ERROR",
                message="Failed to fetch machine specifications",
                payload={
                    "details": str(error),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            ) from error


all_machine_repo = AllMachineRepo()
