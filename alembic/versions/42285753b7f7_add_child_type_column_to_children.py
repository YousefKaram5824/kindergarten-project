"""add child_type column to children

Revision ID: 42285753b7f7
Revises: 
Create Date: 2025-08-31 01:51:02.048648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '42285753b7f7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # إضافة العمود الجديد child_type
    op.add_column(
        "children",
        sa.Column(
            "child_type",
            sa.String(length=50),  # نخزن نوع الطفل كـ string (FULL_DAY / SESSIONS)
            nullable=False,
            server_default="FULL_DAY",  # القيمة الافتراضية
        )
    )


def downgrade() -> None:
    # حذف العمود لو عملنا rollback
    op.drop_column("children", "child_type")
