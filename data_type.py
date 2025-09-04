from sqlalchemy import inspect
from database import Base, engine

inspector = inspect(engine)

for table_name in inspector.get_table_names():
    print(f"Table: {table_name}")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"  - {column['name']}: {column['type']}")
    print("-" * 40)
