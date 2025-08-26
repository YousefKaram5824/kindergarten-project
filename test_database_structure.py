import sqlite3
from database import db

def test_database_structure():
    # Test connection
    if db.connect():
        print('Connected to database successfully')
        
        # Try to execute a simple query
        cursor = db.connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
            result = cursor.fetchone()
            if result:
                print('Students table exists')
                
                # Check the structure of the students table
                cursor.execute('PRAGMA table_info(students)')
                columns = cursor.fetchall()
                print('Students table columns:')
                for col in columns:
                    print(f'  {col[1]} ({col[2]})')
            else:
                print('Students table does not exist')
        except sqlite3.Error as e:
            print(f'Error executing query: {e}')
        
        db.close()
    else:
        print('Failed to connect to database')

if __name__ == "__main__":
    test_database_structure()
