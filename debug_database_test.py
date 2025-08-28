#!/usr/bin/env python3
import os
import sqlite3
from database import db

def test_database():
    print("=== Database Debug Test ===")
    
    # Check if database file exists
    db_path = "kindergarten.db"
    print(f"Database path: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        print(f"File size: {os.path.getsize(db_path)} bytes")
    
    # Test connection
    print("\n=== Testing Connection ===")
    connection_result = db.connect()
    print(f"Connection result: {connection_result}")
    
    if connection_result:
        print("Connection successful!")
        
        # Test creating a student
        print("\n=== Testing Student Creation ===")
        try:
            student_id = db.create_student(
                name="Test Student",
                age=5,
                birth_date="2020-01-01",
                phone="1234567890",
                dad_job="Engineer",
                mum_job="Teacher",
                problem="None",
                photo_path=None
            )
            print(f"Student created with ID: {student_id}")
            
            # Test retrieving students
            print("\n=== Testing Student Retrieval ===")
            students = db.get_all_students()
            print(f"Number of students: {len(students)}")
            for student in students:
                print(f"Student: {student}")
                
        except Exception as e:
            print(f"Error during student operations: {e}")
            
        finally:
            db.close()
    else:
        print("Connection failed!")
        
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_database()
