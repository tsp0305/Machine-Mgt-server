"""create electrical table

Revision ID: 634a29b15217
Revises: ccdbd33de2cc
Create Date: 2025-12-16 14:19:10
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "634a29b15217"
down_revision: Union[str, Sequence[str], None] = "ccdbd33de2cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "electrical",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "machine_id",
            sa.Integer(),
            sa.ForeignKey("machine.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("installed_power_kw_per_machine", sa.Float()),
        sa.Column("installed_power_kw_total", sa.Float()),
        sa.Column("fuse_or_mccb", sa.Integer()),
        sa.Column("power_cable_size_sqmm", sa.String()),
        sa.Column("earth_wire_size_sqmm", sa.String()),
    )

    op.create_index(
        "ix_electrical_machine_id",
        "electrical",
        ["machine_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_electrical_machine_id", table_name="electrical")
    op.drop_table("electrical")
