#!/usr/bin/env python3
from database import db

def test_student_creation():
    print("Testing student creation with photo_path column...")
    
    # Test creating a student
    student_id = db.create_student(
        name="Test Student New",
        age=6,
        birth_date="2019-05-15",
        phone="0987654321",
        dad_job="Doctor",
        mum_job="Nurse",
        problem="None",
        photo_path="/photos/test.jpg"
    )
    
    print(f"Student creation result: {student_id}")
    
    if student_id != -1:
        print("SUCCESS: Student created successfully!")
        
        # Verify the student was added
        students = db.get_all_students()
        print(f"Total students in database: {len(students)}")
        
        # Find the newly created student
        new_student = None
        for student in students:
            if student['name'] == "Test Student New":
                new_student = student
                break
                
        if new_student:
            print(f"✅ Found new student: {new_student}")
            print(f"Photo path: {new_student.get('photo_path', 'Not set')}")
        else:
            print("❌ New student not found in database")
            
    else:
        print("❌ Student creation failed!")

if __name__ == "__main__":
    test_student_creation()
