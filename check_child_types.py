#!/usr/bin/env python3
"""
Script to check child_type values in the database
"""

from database import db_session
from models import Child


def check_child_types():
    """Check child_type values for all children"""
    with db_session() as db:
        children = db.query(Child).all()

        print("📋 Child Type Status:")
        print(f"Total children: {len(children)}")
        print()

        for child in children:
            child_type_display = child.child_type.value if child.child_type else "NULL"
            print(f"ID: {child.id}, Name: {child.name}, Type: {child_type_display}")

        # Count by type
        type_counts = {}
        for child in children:
            child_type = child.child_type.name if child.child_type else "NULL"
            type_counts[child_type] = type_counts.get(child_type, 0) + 1

        print()
        print("📊 Type Distribution:")
        for child_type, count in type_counts.items():
            print(f"{child_type}: {count}")


if __name__ == "__main__":
    check_child_types()
