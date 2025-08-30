from sqlalchemy import inspect
from database import get_db
from models import Base
from tabulate import tabulate


def print_table_data(session, model):
    """Print all data from a given table in a formatted way"""
    table_name = model.__tablename__
    rows = session.query(model).all()
    print(f"\n===== {table_name.upper()} =====")

    if not rows:
        print("⚠️ No data found")
        return

    # Convert SQLAlchemy objects to dict and remove internal state
    data = [r.__dict__.copy() for r in rows]
    for d in data:
        d.pop("_sa_instance_state", None)

    headers = data[0].keys()
    rows_data = [d.values() for d in data]

    print(tabulate(rows_data, headers=headers, tablefmt="grid", showindex=True))


def main():
    db = next(get_db())

    # Show all table names
    inspector = inspect(db.bind)
    print("📋 Existing tables in the database:")
    for table_name in inspector.get_table_names():
        print(f" - {table_name}")

    # Loop through all models registered in Base
    for cls in Base.__subclasses__():
        print_table_data(db, cls)


if __name__ == "__main__":
    main()
