"""update_children_table

Revision ID: 9605ff365338
Revises: 53513cab8f10
Create Date: 2025-09-02 16:12:31.976421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9605ff365338'
down_revision: Union[str, Sequence[str], None] = '53513cab8f10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("children") as batch_op:
        
        batch_op.alter_column(
            "notes",
            type_=sa.String(length=255),
            existing_type=sa.Text(),
            existing_nullable=True
        )
        
        batch_op.add_column(sa.Column("problems", sa.String(length=255), nullable=True))
        
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    
    pass


def downgrade():
    with op.batch_alter_table("children") as batch_op:
    
        batch_op.drop_column("updated_at")
        
        batch_op.drop_column("problems")
        
        batch_op.alter_column(
            "notes",
            type_=sa.Text(),
            existing_type=sa.String(length=255),
            existing_nullable=True
        )    
    pass
