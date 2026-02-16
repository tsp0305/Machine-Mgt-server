"""create machine table

Revision ID: ccdbd33de2cc
Revises: 09adb6fc161a
Create Date: 2025-12-15 20:21:16.033115
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ccdbd33de2cc'
down_revision: Union[str, Sequence[str], None] = '09adb6fc161a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'machine',
        sa.Column('id', sa.Integer(), primary_key=True),

        sa.Column('model_name', sa.String(length=255)),
        sa.Column('description', postgresql.JSONB(), server_default=sa.text("'{}'::jsonb")),
        sa.Column('model', sa.String(length=255)),

        sa.Column('waste_collection_split', sa.String()),
        sa.Column('can_changer_type', sa.String()),
        sa.Column('feed_type', sa.String()),
        sa.Column('wcs_type', sa.String()),
        sa.Column('webdoff_type', sa.String()),

        sa.Column('product_code', sa.Integer()),
        sa.Column('quantity', sa.Integer()),
        sa.Column('weight_kg', sa.Float()),

        sa.Column(
            'dept_id',
            sa.Integer(),
            sa.ForeignKey('department.id', ondelete='CASCADE'),
            nullable=False
        ),
    )

    op.create_index(
        'ix_machine_dept_id',
        'machine',
        ['dept_id']
    )


def downgrade() -> None:
    op.drop_index('ix_machine_dept_id', table_name='machine')
    op.drop_table('machine')
