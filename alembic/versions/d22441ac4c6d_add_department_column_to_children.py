"""add department column to children

Revision ID: d22441ac4c6d
Revises: 45c2997db679
Create Date: 2025-09-10 18:49:50.304726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd22441ac4c6d'
down_revision: Union[str, Sequence[str], None] = '45c2997db679'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('children', sa.Column('department', sa.String(length=100), nullable=True))


def downgrade():
    op.drop_column('children', 'department')
