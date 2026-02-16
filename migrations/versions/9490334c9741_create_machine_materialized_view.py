"""create machine materialized view

Revision ID: 9490334c9741
Revises: 298fe58cf30d
Create Date: 2025-12-22 20:47:44.305019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9490334c9741'
down_revision: Union[str, Sequence[str], None] = '298fe58cf30d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW machine_full_view AS
        SELECT
            -- =====================
            -- MACHINE
            -- =====================
            m.id AS machine_id,
            m.model_name,
            m.description,
            m.model,
            m.waste_collection_split,
            m.can_changer_type,
            m.feed_type,
            m.wcs_type,
            m.webdoff_type,
            m.product_code,
            m.quantity,
            m.weight_kg,
            m.dept_id,

            -- =====================
            -- DEPARTMENT
            -- =====================
            d.id AS department_id,
            d.name AS department_name,
            d.created_at AS department_created_at,
            d.updated_at AS department_updated_at,
            d.deleted_at AS department_deleted_at,
            d.created_by AS department_created_by,
            d.updated_by AS department_updated_by,
            d.deleted_by AS department_deleted_by,

            -- =====================
            -- ELECTRICAL
            -- =====================
            e.id AS electrical_id,
            e.installed_power_kw_per_machine,
            e.installed_power_kw_total,
            e.fuse_or_mccb,
            e.power_cable_size_sqmm,
            e.earth_wire_size_sqmm,

            -- =====================
            -- COMPRESSED AIR
            -- =====================
            ca.id AS compressed_air_id,
            ca.nm3_per_hr_per_machine,
            ca.nm3_per_hr_total,
            ca.pressure_bar,
            ca.incoming_hose_size_mm,

            -- =====================
            -- EXHAUST AIR
            -- =====================
            ex.id AS exhaust_air_id,
            ex.air_m3_sec_per_machine,
            ex.air_m3_sec_total,
            ex.air_to_trench_per_machine,
            ex.air_to_trench_total,
            ex.air_to_filter_per_machine,
            ex.air_to_filter_total,
            ex.pressure_pascal,
            ex.remarks

        FROM machine m
        JOIN department d ON d.id = m.dept_id
        LEFT JOIN electrical e ON e.machine_id = m.id
        LEFT JOIN compressed_air ca ON ca.machine_id = m.id
        LEFT JOIN exhaust_air ex ON ex.machine_id = m.id;
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_machine_full_view_machine_id
        ON machine_full_view (machine_id);
    """)

def downgrade():
    op.execute("""
        DROP INDEX IF EXISTS idx_machine_full_view_machine_id;
    """)
    op.execute("""
        DROP MATERIALIZED VIEW IF EXISTS machine_full_view;
    """)