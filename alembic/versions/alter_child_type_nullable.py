"""add NONE to child_type enum and set as default

Revision ID: add_none_to_child_type
Revises: 42285753b7f7
Create Date: 2025-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_none_to_child_type'
down_revision = '42285753b7f7'
branch_labels = None
depends_on = None


def upgrade():
    # Update existing records to NONE if they are not FULL_DAY or SESSIONS
    # But since the enum is stored as string, we can just change the default
    # First, add NONE to the possible values by updating the column type if needed
    # But since it's a string, we can just change the default
    op.alter_column(
        'children',
        'child_type',
        existing_type=sa.String(length=50),
        server_default='NONE'
    )


def downgrade():
    # Revert default to FULL_DAY
    op.alter_column(
        'children',
        'child_type',
        existing_type=sa.String(length=50),
        server_default='FULL_DAY'
    )
