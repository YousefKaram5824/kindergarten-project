"""add_is_deleted_column_to_childtable

Revision ID: 53513cab8f10
Revises: 42285753b7f7
Create Date: 2025-09-02 16:02:58.190653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53513cab8f10'
down_revision: Union[str, Sequence[str], None] = '42285753b7f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add is_deleted column (default=False)
    op.add_column(
        'children',
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false())
    )
    
    pass    
    


def downgrade():
    # Remove is_deleted column
    op.drop_column('children', 'is_deleted')
    
    pass    
    
