#!/usr/bin/env python3
import sqlite3
import datetime
from database import db

def test_timestamp_fix():
    print("Testing timestamp fix for student creation...")
    
    # Test creating a student
    student_id = db.create_student(
        name="Test Student Timestamp",
        age=5,
        birth_date="2019-01-15",
        phone="1234567890",
        dad_job="Engineer",
        mum_job="Teacher",
        problem="None",
        photo_path=None
    )
    
    print(f"Student creation result: {student_id}")
    
    if student_id != -1:
        print("SUCCESS: Student created successfully!")
        
        # Get the student to check the timestamp
        students = db.get_all_students()
        test_student = None
        for student in students:
            if student['name'] == "Test Student Timestamp":
                test_student = student
                break
                
        if test_student:
            print(f"✅ Found test student: {test_student['name']}")
            print(f"Created at timestamp: {test_student.get('created_at', 'Not set')}")
            
            # Check if timestamp is recent (within last 5 minutes)
            if test_student.get('created_at'):
                try:
                    created_time = datetime.datetime.fromisoformat(test_student['created_at'])
                    current_time = datetime.datetime.now()
                    time_diff = current_time - created_time
                    
                    print(f"Current time: {current_time}")
                    print(f"Time difference: {time_diff}")
                    
                    if time_diff.total_seconds() < 300:  # Less than 5 minutes
                        print("✅ Timestamp is recent (within 5 minutes)")
                    else:
                        print("❌ Timestamp is not recent")
                        
                except ValueError as e:
                    print(f"❌ Error parsing timestamp: {e}")
            else:
                print("❌ No created_at timestamp found")
        else:
            print("❌ Test student not found in database")
            
    else:
        print("❌ Student creation failed!")

if __name__ == "__main__":
    test_timestamp_fix()
