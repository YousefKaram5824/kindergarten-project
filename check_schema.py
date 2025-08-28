#!/usr/bin/env python3
import sqlite3

def check_students_schema():
    conn = sqlite3.connect('kindergarten.db')
    cursor = conn.cursor()
    
    # Check if students table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Students table does not exist!")
        return
    
    # Get table schema
    cursor.execute("PRAGMA table_info(students)")
    columns = cursor.fetchall()
    
    print("Students table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_students_schema()
