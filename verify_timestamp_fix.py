#!/usr/bin/env python3
import datetime
from database import db

def verify_timestamp_fix():
    print("Verifying timestamp fix for student creation...")
    
    # Create a test student
    print("Creating a test student...")
    student_id = db.create_student(
        name="Timestamp Verification Student",
        age=7,
        birth_date="2017-03-20",
        phone="9876543210",
        dad_job="Teacher",
        mum_job="Nurse",
        problem="None"
    )
    
    print(f"Student creation result: {student_id}")
    
    if student_id != -1:
        print("SUCCESS: Student created successfully!")
        
        # Get all students to find our test student
        students = db.get_all_students()
        test_student = None
        for student in students:
            if student['id'] == student_id:
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
                    print(f"Created time: {created_time}")
                    print(f"Time difference: {time_diff}")
                    
                    # Check if the time difference is within a reasonable range (allowing for some small differences)
                    # If the fix is working, the difference should be minimal
                    if abs(time_diff.total_seconds()) < 300:  # Less than 5 minutes
                        print("✅ Timestamp is recent (within 5 minutes) - FIX APPEARS TO BE WORKING")
                        return True
                    else:
                        print("❌ Timestamp difference is significant - FIX MAY NOT BE WORKING")
                        print("This could indicate the timestamp is still being affected by timezone issues")
                        return False
                        
                except ValueError as e:
                    print(f"❌ Error parsing timestamp: {e}")
                    return False
            else:
                print("❌ No created_at timestamp found")
                return False
        else:
            print("❌ Test student not found in database")
            return False
            
    else:
        print("❌ Student creation failed!")
        return False

if __name__ == "__main__":
    success = verify_timestamp_fix()
    if success:
        print("\n🎉 TIMESTAMP FIX VERIFICATION SUCCESSFUL!")
    else:
        print("\n💥 TIMESTAMP FIX VERIFICATION FAILED!")
