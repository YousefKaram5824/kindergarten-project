#!/usr/bin/env python3
import sqlite3

def add_photo_path_column():
    conn = sqlite3.connect('kindergarten.db')
    cursor = conn.cursor()
    
    print("Adding photo_path column to students table...")
    
    try:
        # Add the photo_path column
        cursor.execute("ALTER TABLE students ADD COLUMN photo_path TEXT")
        conn.commit()
        print("Successfully added photo_path column to students table!")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(students)")
        columns = cursor.fetchall()
        print("\nUpdated students table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
    except sqlite3.Error as e:
        print(f"Error adding column: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    add_photo_path_column()
