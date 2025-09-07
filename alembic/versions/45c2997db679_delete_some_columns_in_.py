"""Delete_some_columns_in_IndevidualSession_table

Revision ID: 45c2997db679
Revises: 626d1d4ce3a7
Create Date: 2025-09-07 16:58:03.442371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45c2997db679'
down_revision: Union[str, Sequence[str], None] = '626d1d4ce3a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("individual_sessions") as batch_op:
        batch_op.drop_column("entry_date")
        batch_op.drop_column("personal_photo")
        batch_op.drop_column("child_documents_file")


def downgrade():
    with op.batch_alter_table("individual_sessions") as batch_op:
        batch_op.add_column(sa.Column("entry_date", sa.Date(), nullable=False))
        batch_op.add_column(sa.Column("personal_photo", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("child_documents_file", sa.String(length=255), nullable=True))
