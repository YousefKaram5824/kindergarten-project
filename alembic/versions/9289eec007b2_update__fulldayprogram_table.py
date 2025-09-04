"""Update_ FullDayProgram_table

Revision ID: 9289eec007b2
Revises: 5192f4c16740
Create Date: 2025-09-04 02:09:04.709676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9289eec007b2'
down_revision: Union[str, Sequence[str], None] = '5192f4c16740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("full_day_programs") as batch_op:
        
        batch_op.alter_column("diagnosis",
                              existing_type=sa.Text(),
                              type_=sa.String(500),
                              existing_nullable=True)

        batch_op.alter_column("tests_applied",
                              existing_type=sa.Text(),
                              type_=sa.String(500),
                              existing_nullable=True)

        batch_op.alter_column("training_plan",
                              existing_type=sa.Text(),
                              type_=sa.String(1000),
                              existing_nullable=True)

        batch_op.alter_column("monthly_report",
                              existing_type=sa.Text(),
                              type_=sa.String(1000),
                              existing_nullable=True)

        batch_op.alter_column("notes",
                              existing_type=sa.Text(),
                              type_=sa.String(1000),
                              existing_nullable=True)


        batch_op.add_column(sa.Column("personal_photo", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("birth_certificate", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("father_id_card", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("test_documents", sa.String(255), nullable=True))

        batch_op.add_column(sa.Column("tests_applied_file", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("training_plan_file", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("monthly_report_file", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("child_documents_file", sa.String(255), nullable=True))


def downgrade():
    with op.batch_alter_table("full_day_programs") as batch_op:

        batch_op.alter_column("diagnosis",
                              existing_type=sa.String(500),
                              type_=sa.Text(),
                              existing_nullable=True)

        batch_op.alter_column("tests_applied",
                              existing_type=sa.String(500),
                              type_=sa.Text(),
                              existing_nullable=True)

        batch_op.alter_column("training_plan",
                              existing_type=sa.String(1000),
                              type_=sa.Text(),
                              existing_nullable=True)

        batch_op.alter_column("monthly_report",
                              existing_type=sa.String(1000),
                              type_=sa.Text(),
                              existing_nullable=True)

        batch_op.alter_column("notes",
                              existing_type=sa.String(1000),
                              type_=sa.Text(),
                              existing_nullable=True)

        batch_op.drop_column("personal_photo")
        batch_op.drop_column("birth_certificate")
        batch_op.drop_column("father_id_card")
        batch_op.drop_column("test_documents")

        batch_op.drop_column("tests_applied_file")
        batch_op.drop_column("training_plan_file")
        batch_op.drop_column("monthly_report_file")
        batch_op.drop_column("child_documents_file")
