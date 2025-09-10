"""convert text columns to string in finance tables

Revision ID: 15c039bac931
Revises: d22441ac4c6d
Create Date: 2025-09-10 18:56:20.399831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15c039bac931'
down_revision: Union[str, Sequence[str], None] = 'd22441ac4c6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # DailyVisit
    with op.batch_alter_table("daily_visits", recreate="always") as batch_op:
        batch_op.alter_column("purpose", type_=sa.String(255))
        batch_op.alter_column("notes", type_=sa.String(255))

    # DailyFinance
    with op.batch_alter_table("daily_finances", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.String(255))

    # MonthlyFinanceFullDay
    with op.batch_alter_table("monthly_finance_full_day", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.String(255))

    # MonthlyFinanceIndividual
    with op.batch_alter_table("monthly_finance_individual", recreate="always") as batch_op:
        batch_op.alter_column("specialists_details", type_=sa.String(500))
        batch_op.alter_column("notes", type_=sa.String(255))

    # MonthlyFinanceOverall
    with op.batch_alter_table("monthly_finance_overall", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.String(255))


def downgrade():
    # DailyVisit
    with op.batch_alter_table("daily_visits", recreate="always") as batch_op:
        batch_op.alter_column("purpose", type_=sa.Text)
        batch_op.alter_column("notes", type_=sa.Text)

    # DailyFinance
    with op.batch_alter_table("daily_finances", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.Text)

    # MonthlyFinanceFullDay
    with op.batch_alter_table("monthly_finance_full_day", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.Text)

    # MonthlyFinanceIndividual
    with op.batch_alter_table("monthly_finance_individual", recreate="always") as batch_op:
        batch_op.alter_column("specialists_details", type_=sa.Text)
        batch_op.alter_column("notes", type_=sa.Text)

    # MonthlyFinanceOverall
    with op.batch_alter_table("monthly_finance_overall", recreate="always") as batch_op:
        batch_op.alter_column("notes", type_=sa.Text)
