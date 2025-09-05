#!/usr/bin/env python3
"""
Script to reset all children-related data in the database.
This will delete all records from children and related tables.
"""

from database import db_session, create_tables
from models import (
    Child, FullDayProgram, IndividualSession,
    DailyVisit, DailyFinance
)

def reset_children_data():
    """Delete all children and related data"""
    with db_session() as db:
        try:
            # Delete in order to respect foreign key constraints
            print("Deleting daily finances...")
            db.query(DailyFinance).delete()

            print("Deleting daily visits...")
            db.query(DailyVisit).delete()

            print("Deleting individual sessions...")
            db.query(IndividualSession).delete()

            print("Deleting full day programs...")
            db.query(FullDayProgram).delete()

            print("Deleting children...")
            db.query(Child).delete()

            # Commit all changes
            db.commit()
            print("✅ All children data has been successfully deleted!")

        except Exception as e:
            db.rollback()
            print(f"❌ Error occurred: {e}")
            return False

    return True

if __name__ == "__main__":
    print("🔄 Starting database reset for children data...")
    success = reset_children_data()
    if success:
        print("🎉 Database reset completed successfully!")
    else:
        print("💥 Database reset failed!")
