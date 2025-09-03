"""change notes columns from Text to String

Revision ID: c63adfeac836
Revises: fe56ecb50313
Create Date: 2025-09-03 21:57:08.969621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c63adfeac836'
down_revision: Union[str, Sequence[str], None] = 'fe56ecb50313'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # TrainingTool.notes
    op.alter_column(
        "training_tools",
        "notes",
        existing_type=sa.Text(),
        type_=sa.String(length=1000),
        existing_nullable=True
    )

    # ToolForSale.notes
    op.alter_column(
        "tools_for_sale",
        "notes",
        existing_type=sa.Text(),
        type_=sa.String(length=1000),
        existing_nullable=True
    )

    # UniformForSale.notes
    op.alter_column(
        "uniforms_for_sale",
        "notes",
        existing_type=sa.Text(),
        type_=sa.String(length=1000),
        existing_nullable=True
    )

    # BookForSale.notes
    op.alter_column(
        "books_for_sale",
        "notes",
        existing_type=sa.Text(),
        type_=sa.String(length=1000),
        existing_nullable=True
    )    
    



def downgrade():
    # TrainingTool.notes
    op.alter_column(
        "training_tools",
        "notes",
        existing_type=sa.String(length=1000),
        type_=sa.Text(),
        existing_nullable=True
    )

    # ToolForSale.notes
    op.alter_column(
        "tools_for_sale",
        "notes",
        existing_type=sa.String(length=1000),
        type_=sa.Text(),
        existing_nullable=True
    )

    # UniformForSale.notes
    op.alter_column(
        "uniforms_for_sale",
        "notes",
        existing_type=sa.String(length=1000),
        type_=sa.Text(),
        existing_nullable=True
    )

    # BookForSale.notes
    op.alter_column(
        "books_for_sale",
        "notes",
        existing_type=sa.String(length=1000),
        type_=sa.Text(),
        existing_nullable=True
    )   
