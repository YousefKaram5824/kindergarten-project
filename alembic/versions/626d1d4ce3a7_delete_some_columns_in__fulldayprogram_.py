"""Delete_some_columns_in_ FullDayProgram_table

Revision ID: 626d1d4ce3a7
Revises: c1672ed1fae4
Create Date: 2025-09-07 16:47:23.314755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '626d1d4ce3a7'
down_revision: Union[str, Sequence[str], None] = 'c1672ed1fae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("full_day_programs") as batch_op:
        batch_op.drop_column("entry_date")
        batch_op.drop_column("personal_photo")
        batch_op.drop_column("test_documents")
        batch_op.drop_column("child_documents_file")


def downgrade():
    with op.batch_alter_table("full_day_programs") as batch_op:
        batch_op.add_column(sa.Column("entry_date", sa.Date(), nullable=False))
        batch_op.add_column(sa.Column("personal_photo", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("test_documents", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("child_documents_file", sa.String(length=255), nullable=True))
