"""create compressed_air table

Revision ID: fe339cb0033d
Revises: 634a29b15217
Create Date: 2025-12-16 14:25:06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fe339cb0033d"
down_revision: Union[str, Sequence[str], None] = "634a29b15217"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "compressed_air",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "machine_id",
            sa.Integer(),
            sa.ForeignKey("machine.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("nm3_per_hr_per_machine", sa.Float()),
        sa.Column("nm3_per_hr_total", sa.Float()),
        sa.Column("pressure_bar", sa.Float()),
        sa.Column("incoming_hose_size_mm", sa.Float()),
    )

    op.create_index(
        "ix_compressed_air_machine_id",
        "compressed_air",
        ["machine_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_compressed_air_machine_id", table_name="compressed_air")
    op.drop_table("compressed_air")
