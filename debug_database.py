#!/usr/bin/env python3
import os
import sqlite3
import sys

def debug_database():
    """Debug function to test database creation and output"""
    db_path = "kindergarten.db"
    
    # Create output file
    with open("debug_output.txt", "w") as f:
        f.write(f"Debugging database creation at: {db_path}\n")
        f.write(f"Current working directory: {os.getcwd()}\n")
        
        # Check if file exists
        if os.path.exists(db_path):
            f.write(f"Database file already exists at: {db_path}\n")
            f.write(f"File size: {os.path.getsize(db_path)} bytes\n")
            return True
        
        # Try to create database
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            # Create test table
            cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
            connection.commit()
            connection.close()
            
            f.write(f"Database created successfully at: {db_path}\n")
            f.write(f"File size: {os.path.getsize(db_path)} bytes\n")
            return True
            
        except Exception as e:
            f.write(f"Error creating database: {e}\n")
            return False

if __name__ == "__main__":
    success = debug_database()
    if success:
        print("Debug completed successfully - check debug_output.txt")
    else:
        print("Debug failed - check debug_output.txt")
    sys.exit(0 if success else 1)
