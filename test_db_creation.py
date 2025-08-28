#!/usr/bin/env python3
import os
import sqlite3
import sys

def test_database_creation():
    db_path = "kindergarten.db"
    
    print(f"Testing database creation at: {db_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if file exists before
    if os.path.exists(db_path):
        print(f"Database file already exists at: {db_path}")
        return True
    
    # Try to create the database
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Create a simple table to test
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)")
        connection.commit()
        connection.close()
        
        print(f"Database created successfully at: {db_path}")
        print(f"File size: {os.path.getsize(db_path)} bytes")
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    success = test_database_creation()
    sys.exit(0 if success else 1)
