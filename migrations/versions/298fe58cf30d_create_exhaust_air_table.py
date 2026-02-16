from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "298fe58cf30d"
down_revision: Union[str, Sequence[str], None] = "fe339cb0033d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exhaust_air",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "machine_id",
            sa.Integer(),
            sa.ForeignKey("machine.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("air_m3_sec_per_machine", sa.Float()),
        sa.Column("air_m3_sec_total", sa.Float()),
        sa.Column("air_to_trench_per_machine", sa.Float()),
        sa.Column("air_to_trench_total", sa.Float()),
        sa.Column("air_to_filter_per_machine", sa.Float()),
        sa.Column("air_to_filter_total", sa.Float()),
        sa.Column("pressure_pascal", sa.Float()),
        sa.Column("remarks", sa.String()),
    )

    # ⚠ Corrected table name here to match create_table
    op.create_index(
        "ix_exhaust_air_machine_id",
        "exhaust_air",
        ["machine_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_exhaust_air_machine_id", table_name="exhaust_air")
    op.drop_table("exhaust_air")
