"""remove tool_number column

Revision ID: fecdd212a77c
Revises: 15c039bac931
Create Date: 2025-09-11 22:23:04.925259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fecdd212a77c'
down_revision: Union[str, Sequence[str], None] = '15c039bac931'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('training_tools', 'tool_number')
    op.drop_column('tools_for_sale', 'tool_number')


def downgrade():
    op.add_column('training_tools', sa.Column('tool_number', sa.String(length=50)))
    op.add_column('tools_for_sale', sa.Column('tool_number', sa.String(length=50)))
