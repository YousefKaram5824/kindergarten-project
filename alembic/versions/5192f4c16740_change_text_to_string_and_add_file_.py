""" change Text to String and add file columns

Revision ID: 5192f4c16740
Revises: fe56ecb50313
Create Date: 2025-09-04 01:29:17.545866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5192f4c16740'
down_revision: Union[str, Sequence[str], None] = 'fe56ecb50313'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # TrainingTool.notes
    with op.batch_alter_table("training_tools") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.Text(),
            type_=sa.String(length=1000),
            existing_nullable=True
        )

    # ToolForSale.notes
    with op.batch_alter_table("tools_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.Text(),
            type_=sa.String(length=1000),
            existing_nullable=True
        )

    # UniformForSale.notes
    with op.batch_alter_table("uniforms_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.Text(),
            type_=sa.String(length=1000),
            existing_nullable=True
        )

    # BookForSale.notes
    with op.batch_alter_table("books_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.Text(),
            type_=sa.String(length=1000),
            existing_nullable=True
        )    


def downgrade():
    # TrainingTool.notes
    with op.batch_alter_table("training_tools") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.String(length=1000),
            type_=sa.Text(),
            existing_nullable=True
        )

    # ToolForSale.notes
    with op.batch_alter_table("tools_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.String(length=1000),
            type_=sa.Text(),
            existing_nullable=True
        )

    # UniformForSale.notes
    with op.batch_alter_table("uniforms_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.String(length=1000),
            type_=sa.Text(),
            existing_nullable=True
        )

    # BookForSale.notes
    with op.batch_alter_table("books_for_sale") as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=sa.String(length=1000),
            type_=sa.Text(),
            existing_nullable=True
        )
