#!/usr/bin/env python3
"""
Script to check the current status of the database
"""

from database import db_session
from models import Child, FullDayProgram, IndividualSession, DailyVisit, DailyFinance


def check_db_status():
    """Check current database status"""
    with db_session() as db:
        children_count = db.query(Child).count()
        full_day_count = db.query(FullDayProgram).count()
        sessions_count = db.query(IndividualSession).count()
        visits_count = db.query(DailyVisit).count()
        finances_count = db.query(DailyFinance).count()

        print("📊 Database Status:")
        print(f"Children: {children_count}")
        print(f"Full Day Programs: {full_day_count}")
        print(f"Individual Sessions: {sessions_count}")
        print(f"Daily Visits: {visits_count}")
        print(f"Daily Finances: {finances_count}")

        if children_count == 0:
            print("✅ Children table is empty!")
        else:
            print("⚠️  Children table still has data!")


if __name__ == "__main__":
    check_db_status()
