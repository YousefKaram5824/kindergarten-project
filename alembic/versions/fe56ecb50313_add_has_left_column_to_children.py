"""add has_left column to children

Revision ID: fe56ecb50313
Revises: 9605ff365338
Create Date: 2025-09-02 17:18:12.106180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe56ecb50313'
down_revision: Union[str, Sequence[str], None] = '9605ff365338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("children") as batch_op:
        batch_op.add_column(sa.Column("has_left", sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    with op.batch_alter_table("children") as batch_op:
        batch_op.drop_column("has_left")
